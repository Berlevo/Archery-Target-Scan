# Archery Target Scan
Archery Target Scan is a python code which returns the point on the target. Our target has 5 circles.

## Scanning
<p align="justify"> In target scanning part i have used hough circle transform and template matching to find the 5 circles on image. I have used blop detection to find the black dots on the target. </p>


Example Target Image:

![target2](https://user-images.githubusercontent.com/42059887/206720181-b62c156c-7f1b-47df-82eb-23894ca96db2.jpg)

### Hough Circle Transform
<p align="justify"> In hough circle transform, i have created a loop to find 5 circles on the target. This loop takes 500 as max circle radius to find in the target and subtractes 50 from this radius until it reaches 0. In each iteration hough circle transform will try to find circles on the target. However there won't be 5 circles on the target after using hough circle tranform. There will be circles in between 0 to 10. Therefore, in order to get the accureate results i have looked each circles radius and center points. If 5 circles center point is very close to each other then i have taken those circles. Although if their radiuses are very close to each other i have taken them as well. </p>

Example Result From Hough Circle Transform:

![detected-circles-1](https://user-images.githubusercontent.com/42059887/206724354-a572764d-a008-409f-acc8-378a4c980f14.png)

### Template Matching
<p align="justify"> In template matching, i have used a clear target as our template. I have tried to find this template on our target. However, i couldn't found template on our target because of the size diffrence. My target image size was big in terms of height and my template image width was bigger than target image. Therefore, i have created an iteration which makes template image smaller in each iteration. To get the wanted results, after using template matching i have implemented hough circle transform. Thus, the code won't try to small template every time because if there is 5 circles on the image then it means, template matching and hough circle transform worked correct. </p>

Template Image:

![targetss](https://user-images.githubusercontent.com/42059887/206720025-57febfdf-e537-4831-85a6-c56988a79d76.jpg)

Template Matching Result On Target Image:

![TemplateMatching](https://user-images.githubusercontent.com/42059887/206727094-daa69f19-cc5c-4188-85d7-bda15b8a0170.png)

Hough Circle Transform After Template Matching:

![Hough_circle](https://user-images.githubusercontent.com/42059887/206727462-b8f9da28-aa1b-454d-9014-f9d25493d14d.png)

### Blop Detection
<p align="justify"> In blop detection i have used simple thresholding to find the black dots on the target. I have set the minimum pixel for thresholding to 30 and maximum pixel for thresholding to 255. For thresholding method i have used THRESH_BINARY. </p>

Cropted Target Image:

![blopdetect](https://user-images.githubusercontent.com/42059887/206837583-2f6fcd71-3c8b-4c54-a110-e60ed39fe090.png)

Thresholding Target Image:

![thres](https://user-images.githubusercontent.com/42059887/206837628-d5d0c93a-2042-4b6a-a1cb-dd9a6d44e149.png)

Blop Detection On Target Image:

![Plopdetect](https://user-images.githubusercontent.com/42059887/206837635-7c93b830-6305-48a1-86e2-107735bfff51.png)

### Finding The Score
<p align="justify"> To find the score on the target, i find the blop center point and target center point. Then, i have used analytical geometry to find the distance between these two points. After finding the distance i have compared this with targets circle radiuses.</p>

Scan Result:

![7 Score-1](https://user-images.githubusercontent.com/42059887/206857118-1a513eb2-f005-468b-a5f8-09d76b6c607f.png)



