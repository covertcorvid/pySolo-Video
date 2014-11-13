__author__ = 'quentin'


import numpy as np
import cv2
import cv

class ROI(object):

    def __init__(self, polygon, value=None, orientation = None, regions=None):

        # TODO if we do not need polygon, we can drop it
        self._polygon = np.array(polygon)
        if len(self._polygon.shape) == 2:
            self._polygon = self._polygon.reshape((self._polygon.shape[0],1,self._polygon.shape[1]))

        self._value = value
        x,y,w,h = cv2.boundingRect(self._polygon)

        self._mask = np.zeros((h,w), np.uint8)
        cv2.drawContours(self._mask, [self._polygon], 0, 255,-1,offset=(-x,-y))

        self._rectangle = x,y,w,h
        # todo NOW! sort rois by value. if no values, left to right/ top to bottom!

        self.idx = None

    def bounding_rect(self):
        raise NotImplementedError


    def mask(self):
        return self._mask

    @property
    def offset(self):
        x,y,w,h = self._rectangle
        return x,y

    @property
    def polygon(self):

        return self._polygon


    @property
    def longest_axis(self):
        x,y,w,h = self._rectangle
        return float(max(w, h))
    @property
    def rectangle(self):
        return self._rectangle



    def set_value(self, new_val):
        self._value = new_val

    @property
    def value(self):
        return self._value

    def __call__(self,img):
        x,y,w,h = self._rectangle
        out = img[y : y + h, x : x +w]


        assert(out.shape[0:2] == self._mask.shape)

        return out, self._mask


class BaseROIBuilder(object):

    def __call__(self, camera):

        accum = []
        if isinstance(camera, np.ndarray):
            accum = camera

        else:
            for i, (_, frame) in enumerate(camera):
                accum.append(frame)
                if i  >= 10:
                    break

            accum = np.median(np.array(accum),0).astype(np.uint8)

        rois = self._rois_from_img(accum)
        rois_w_no_value = [r for r in rois if r.value is None]

        if len(rois_w_no_value) > 0:
            rois = self._spatial_sorting(rois)
        else:
            rois = self._value_sorting(rois)

        for i,r in enumerate(rois):
            r.idx =i
        return rois



    def _rois_from_img(self,img):
        raise NotImplementedError

    def _spatial_sorting(self, rois):
        out = []
        for i, sr in enumerate(sorted(rois, lambda  a,b: a.rectangle[0] - b.rectangle[0])):
            if sr.value is None:
                sr.set_value(i)
            out.append(sr)
        return out

    def _value_sorting(self, rois):
        out = []
        for i, sr in enumerate(sorted(rois, lambda  a,b: a.value - b.value)):
            out.append(sr)
        return out


class DefaultROIBuilder(BaseROIBuilder):

    def _rois_from_img(self,img):
        h, w = img.shape[0],img.shape[1]
        return[
            ROI([
                (   0,        0       ),
                (   0,        h -1    ),
                (   w - 1,    h - 1   ),
                (   w - 1,    0       )]
        )]



def show(im, t=-1):

    cv2.imshow("test", im)
    cv2.waitKey(t)


class SleepDepROIBuilder(BaseROIBuilder):
    _n_rois = 32
    _adaptive_med_rad = 0.070
    _min_food_tip_area = 1e-4
    _max_food_tip_area = 2e-3
    _min_food_tip_ar = 0.65
    _tube_over_tip_ratio = 1/3.5
    def _rois_from_img(self,im):


        rot_mat= self._best_image_rotation(im)

        rois = self._make_rois(im, rot_mat)
        return rois

    def _score_food_tip_blobs(self,contour, im):
        h, w = im.shape[0:2]
        area = cv2.contourArea(contour)
        if area <0 :
            return 0
        perim = cv2.arcLength(contour,True)

        area_ratio = area / (1.0*w*h)

        if area_ratio < self._min_food_tip_area:
            return 0

        if area_ratio > self._max_food_tip_area:
            return 0

        x,y,w,h  = cv2.boundingRect(contour)


        aspect_ratio = min(w,h) / float(max(w,h))
        if aspect_ratio < self._min_food_tip_ar:
             return 0

        return 1

    def _find_blobs(self, im, scoring_fun):
        grey= cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        rad = int(self._adaptive_med_rad * im.shape[1])
        if rad % 2 == 0:
            rad += 1

        cv2.erode(grey, None,grey, iterations=2)
        cv2.dilate(grey,None,grey, iterations=2)
        med = cv2.medianBlur(grey, rad)
        cv2.subtract(med, grey, dst = med)

        bin = grey
        score_map = np.zeros_like(bin)
        for t in range(0, 255,1):
            cv2.threshold(med, t, 255,cv2.THRESH_BINARY,bin)
            if np.count_nonzero(bin) < self._adaptive_med_rad**2  * im.shape[0] * im.shape[1]:
                break
            if np.count_nonzero(bin) > 0.3 * im.shape[0] * im.shape[1]:
                continue
            contours, h = cv2.findContours(bin,cv2.RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_SIMPLE)

            bin.fill(0)
            for c in contours:
                score = scoring_fun(c, im)
                if score >0:
                    cv2.drawContours(bin,[c],0,score,-1)
            cv2.add(bin, score_map,score_map)
        cv2.dilate(score_map,None,score_map, iterations=2)
        cv2.erode(score_map, None,score_map, iterations=2)
        return score_map

    def _best_image_rotation(self, im):
        score_map = self._find_blobs(im, self._score_food_tip_blobs)
        cv2.threshold(score_map, -1,255,cv2.THRESH_OTSU | cv2.THRESH_BINARY, score_map)

        dst = cv2.distanceTransform(score_map, cv2.cv.CV_DIST_L2, cv2.cv.CV_DIST_MASK_PRECISE)
        return  self._find_best_angle(dst)

    def _find_best_angle(self, im, min_theta=-30, max_theta=+30, theta_incr=.5 ):

        min_entr, best_rot_mat, out = -np.Inf , None, None
        for theta in np.arange(min_theta, max_theta, theta_incr):
            M= cv2.getRotationMatrix2D((im.shape[1]/2,im.shape[0]/2), theta,  1)
            rotated_im = cv2.warpAffine(im,M, (im.shape[1],im.shape[0]))
            row_means = np.mean(rotated_im,1)
            row_means /= np.sum(row_means)

            entr =  np.sum(np.log2(row_means+1e-10) * row_means)

            if entr > min_entr:
                min_entr = entr
                best_rot_mat = M
        return best_rot_mat



    def _score_cotton_wool_blobs(self,contour, im, w_food_tip):
        x,y,w,h = cv2.boundingRect(contour)

        if w > w_food_tip:
            return 0
        if w < w_food_tip/3.:

            return 0
        if h > w_food_tip *5.0:
            return 0
        if h < w_food_tip/5.0:
            return 0
        area = cv2.contourArea(contour)

        perim = cv2.arcLength(contour,True)


        circul =  4 * np.pi * area / perim **2
        if circul < .25:
            return 0
        return 1

    def _find_cotton_plugs(self, im, w_food_tip, top_pos, bottom_pos):

        score_fun = lambda c, im: self._score_cotton_wool_blobs(c, im, w_food_tip)

        score_mat = self._find_blobs(im,score_fun)

        score_mat[0:top_pos+w_food_tip,:] = 0
        score_mat[bottom_pos - w_food_tip:,:] = 0
        return score_mat


    def _make_rois(self, im, rot_mat):

        rotated_im = cv2.warpAffine(im, rot_mat, (im.shape[1],im.shape[0]))

        score_map = self._find_blobs(rotated_im,self._score_food_tip_blobs)
        m = np.mean(score_map,1)


        t = np.percentile(m, 100 * (1. - self._adaptive_med_rad * 2))

        mm = np.zeros_like(m)
        mm[m >= t] = 1


        # find continuous regions in vector:
        stop_start = []
        area_under_curves = []
        start = None

        for i, v in enumerate(np.diff(mm)):
            if v == 1:
                start = i
            elif v == -1 or i == m.size:
                stop = i
                if start is not None:
                    stop_start.append((start,stop))
                    area_under_curves.append(np.sum(m[start:stop]))
                start = None

        if len(stop_start) < 2:
            raise Exception("At leat one row of tube tips could not be detected")

        rank_auc = np.argsort(area_under_curves)
        rank_auc = rank_auc[::-1]

        tube_row_mat = np.zeros_like(score_map)

        for r in rank_auc[0:2]:
            start,stop = stop_start[r]
            tube_row_mat[start:stop,:] = 255


        cv2.threshold(score_map, 5,255,cv2.THRESH_BINARY, score_map)

        # show(score_map / 2 + tube_row_mat/2)
        cv2.bitwise_and(score_map, tube_row_mat, tube_row_mat)

        contours, h = cv2.findContours(np.copy(tube_row_mat),cv2.RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_SIMPLE)

        areas, centres, wh = [], [], []


        for c in contours:
            if self._score_food_tip_blobs(c, tube_row_mat) <1:
                raise Exception("At least one row of tube tips could not be detected")
                continue
            moms = cv2.moments(c)

            if moms["m00"] == 0:
                continue

            xy = moms["m10"]/moms["m00"]+ 1j *  moms["m01"]/moms["m00"]
            centres.append(xy)
            x0,y0,w,h =  cv2.boundingRect(c)
            wh.append(w + 1j * h)
            areas.append(moms["m00"])


        if len(centres) < self._n_rois:
            raise Exception("Wrong number of ROIs")
        elif len(centres) > self._n_rois:
            ranks = np.argsort(areas)[::-1]
            ranks = ranks[0:self._n_rois]
            centres = np.array(centres)[ranks]
            wh = np.array(wh)[ranks]

        average_wh = np.median(wh)


        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness,labels,centroids = cv2.kmeans(np.imag(centres).astype(np.float32),2,criteria,attempts=3,flags=flags)
        centroids = centroids.flatten()
        top_lab = np.argmin(centroids)
        top_pos = int(np.median([tx for tx,l in zip(np.imag(centres),labels) if l == top_lab]))
        bottom_pos = int(np.median([tx for tx,l in zip(np.imag(centres),labels) if l != top_lab]))

        aw, ah = np.real(average_wh), np.imag(average_wh)
        half_w = int(aw*0.5)

        wool_plugs = self._find_cotton_plugs(rotated_im , aw, top_pos, bottom_pos)
        wool_plugs[0: top_pos + aw] = 0
        wool_plugs[bottom_pos - aw:] = 0

        cv2.threshold(wool_plugs, 5,255,cv2.THRESH_BINARY,wool_plugs)

        mid_pos = (top_pos + bottom_pos) / 2


        all_tube_widths = []
        all_tube_heights= []
        wool_xs = []


        all_plugs_contours, hiera = cv2.findContours(np.copy(wool_plugs), cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)


        for xfd, l in zip(np.real(centres), labels):

            if l == top_lab:
                y_start = mid_pos
                y_stop = bottom_pos - half_w * 2

            else:
                y_start = top_pos + half_w * 2
                y_stop = mid_pos

            sub_img = wool_plugs[ y_start : y_stop, xfd-half_w : xfd + half_w ]
            contours, hiera = cv2.findContours(np.copy(sub_img), cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)



            if len(contours) < 1:
                raise Exception("Cotton Wool plug not found")

            areas = []
            for c in contours:
                if c.shape[0] < 3:
                    areas.append(0)
                else:
                    areas.append(cv2.contourArea(c))

            max_area_idx = np.argmax(areas)
            ct = contours[max_area_idx]

            moms = cv2.moments(ct)

            x, y = moms["m10"]/moms["m00"],   moms["m01"]/moms["m00"]



            dists = [cv2.pointPolygonTest(rc,(x + xfd-half_w,  y+y_start ), True) for rc in all_plugs_contours]
            real_contour = all_plugs_contours[np.argmax(dists)]
            assert(real_contour is not None)


            cv2.drawContours(rotated_im, [real_contour],-1, (0,255,255),2)
            rotated_im[ y_start : y_stop, xfd-half_w : xfd + half_w,: ] /= 2
            # cv2.drawContours(rotated_im, [real_contour],-1, (0,255,255),2)

            # rotated_im[ y_start : y_stop, xfd-half_w : xfd + half_w,: ] /= 2
            # cv2.circle(rotated_im,(int(x + xfd-half_w), int(y+y_start)),3, (0,255,255),2)
            # show(rotated_im)

            (x,y), (w,h), phi = cv2.fitEllipse(real_contour)

            x -= ( xfd-half_w)
            y -= y_start
            #

            wool_xs.append(xfd - half_w + x)
            all_tube_widths.append(w)
            th = y  + h

            if l == top_lab:
                th  = th + mid_pos - top_pos
            else:
                th  = sub_img.shape[0]-th + (bottom_pos - mid_pos)

            all_tube_heights.append(th)

        average_tube_half_w = 0.8 * np.median(all_tube_widths)/2.0
        average_tube_h = np.median(all_tube_heights)


        final_mask = np.zeros_like(tube_row_mat)
        tmp_mask = np.zeros_like(tube_row_mat)

        for xfd, xw, l in zip(np.real(centres), wool_xs, labels):

            if l == top_lab:
                a = (xfd - average_tube_half_w , top_pos  + aw)
                b = (xfd + average_tube_half_w , top_pos  + aw)
                c = (xw + average_tube_half_w , top_pos  + average_tube_h)
                d = (xw - average_tube_half_w , top_pos + average_tube_h)

            else:
                a = (xw - average_tube_half_w , bottom_pos - average_tube_h)
                b = (xw + average_tube_half_w , bottom_pos - average_tube_h)
                c = (xfd + average_tube_half_w , bottom_pos - aw)
                d = (xfd - average_tube_half_w , bottom_pos - aw)

            pol = np.array([a,b,c,d]).astype(np.int)
            pol = pol.reshape(4,1,2)
            tmp_mask.fill(0)
            cv2.drawContours(tmp_mask , [pol], 0,255,-1)

            cv2.bitwise_xor(tmp_mask,final_mask, final_mask)
            cv2.drawContours(final_mask , [pol], 0,0,1)
            show(final_mask, 1)

        show(final_mask/3  + wool_plugs/3, 200)


        # fixme do not just draw! try to split rois appart, at least 5 px
        i_rot_mat = cv2.invertAffineTransform(rot_mat)

        cv2.warpAffine(final_mask, i_rot_mat, (im.shape[1],im.shape[0]),final_mask)
        cv2.threshold(final_mask,254,255,cv2.THRESH_BINARY,final_mask)
        contours, hiera = cv2.findContours(np.copy(final_mask), cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)

        rois = []
        for c in contours:
            rois.append(ROI(c, None))

        if len(rois) != self._n_rois:
            raise Exception("Unknown error, the total number of ROIs is different from the target")
        return rois


class ImgMaskROIBuilder(BaseROIBuilder):
    """
    Initialised with an grey-scale image file.
    Each continuous region is used as a ROI.
    The colour of the ROI determines it's index
    """


    def __init__(self, mask_path):
        self._mask = cv2.imread(mask_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    def _rois_from_img(self,img):
        if len(self._mask.shape) == 3:
            self._mask = cv2.cvtColor(self._mask, cv2.COLOR_BGR2GRAY)



        contours, hiera = cv2.findContours(np.copy(self._mask), cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)

        rois = []
        for c in contours:
            tmp_mask = np.zeros_like(self._mask)
            cv2.drawContours(tmp_mask, [c],0, 1)

            value = int(np.median(self._mask[tmp_mask > 0]))

            rois.append(ROI(c, value))
        return rois


