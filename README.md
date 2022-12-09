# Archery Target Scan
Archery Target Scan is a python code which returns the point number on the target. Our target has 5 circles.

## Scanning
In scanning part i have used hough circle transform and template matching.

Example Target Image:

![target2](https://user-images.githubusercontent.com/42059887/206720181-b62c156c-7f1b-47df-82eb-23894ca96db2.jpg)

### Hough Circle Transform
In hough circle transform, i have created a loop to find 5 circles on the target. This loop takes 500 as max circle radius to find in the target and subtractes 50 from this radius until it reaches 0. In each iteration hough circle transform will try to find circles on the target. However there won't be 5 circles on the target after using hough circle tranform. There will be circles in between 0 to 10. Therefore, in order to get the accureate results i have looked each circles radius and center points. If 5 circles center point is very close to each other then i have taken those circles. Although if their radiuses are very close to each other i have taken them as well.

Example result from hough circle transform:

![detected-circles-1](https://user-images.githubusercontent.com/42059887/206724354-a572764d-a008-409f-acc8-378a4c980f14.png)

### Template Matching
In template matching, i have used a clear target as our template. I have tried to find this template on our target. However, i couldn't found template on our target because of the size diffrence. My target image size was big in terms of height and my template image width was bigger than target image. Therefore, i have created an iteration which makes template image smaller in each iteration. To get the wanted results, after using template matching i have implemented hough circle transform. Thus, the code won't try to small template every time because if there is 5 circles on the image then it means, template matching and hough circle transform worked correct.

Template Image:

![targetss](https://user-images.githubusercontent.com/42059887/206720025-57febfdf-e537-4831-85a6-c56988a79d76.jpg)

Template Matching Result On Target Image:

![TemplateMatching](https://user-images.githubusercontent.com/42059887/206727094-daa69f19-cc5c-4188-85d7-bda15b8a0170.png)

Hough Circle Transform After Template Matching:

![Hough_circle](https://user-images.githubusercontent.com/42059887/206727462-b8f9da28-aa1b-454d-9014-f9d25493d14d.png)



