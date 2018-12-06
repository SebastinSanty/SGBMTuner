# SGBMTuner
A parameter tuning webapp for StereoSGBM

The definition of parameters are missing from OpenCV. Check these to make the changes:
* **preFilterCap**: Clips the output to \[-preFilterCap, preFilterCap\]. 
* **uniquenessRatio**: Computed disparity d* is accepted only if SAD(d)>=SAD(d*)*(1+uniquenessRatio/100) for any d!=d+/-1. 
* **speckleRange, speckleWindowSize**: Parameters of   the OpenCV   function filterSpeckles  which  is  used  to  post  process the  disparity  map.  It  replaces blobs  of  similar  disparities  (the  difference  of  two adjacent  values  does  not exceed speckleRange) whose size is less or equal to speckleWindowSize (the number of pixels forming the blob) by the invalid disparity value. 
* **disp12MaxDiff**: A left-right check is performed. Pixels are matched from left to  right  image  and  then  from  the  right  back  to  the left.  The  disparity  value  is accepted only if the distance of the first match and the distance of the second match have maximum difference of disp12MaxDiff.
* **fullDP**:  If  set  to  true,  the  algorithm  considers  eight  directions  instead  of  five (like the original) but with higher memory consumption. 
* **P1**: Penalty for small disparity changes. 
* **P2**: Penalty for higher disparity changes
