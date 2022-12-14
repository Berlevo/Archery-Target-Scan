import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math

All_circle_radius = []
Selected_circle_radius = []
Removed_Circle_radius_points = []
center_points = []
center_points_x = []
center_points_y = []
Removed_Center_Points = []
Circle_locations = []
updated_Circle_radius_points = []
cropImg = ""
try_templateMatching = True
done = True
isTemplate = 0
Scored_Points = []
template_scale_percent = 100
targetName = ""
template = ""
croptedImg = ""
thresh1 = ""
farkW = 0
farkH = 0
isTemplate = 0
farkList = []
farkList1 = []

def main():
    global targetName, template, done, cropImg
    #target1.jpg
    #New_target1.jfif
    
    #"C:\\Users\\Berlevo\\Desktop\\Bitirme\\Ders\\TargetImage\\target1.jpg"
    targetName = "C:\\Users\\Berlevo\\Desktop\\Bitirme\\Ders\\TargetImage\\NewTarget7.jpg"
    img = cv.imread(targetName, 0)
    template = cv.imread("C:\\Users\\Berlevo\\Desktop\\Bitirme\\Ders\\TargetImage\\targetss.jpg",0)

    # Check if image size is bigger than 1000
    if img.shape[0] > 1000 and img.shape[1] > 1000:
        template_width = int(img.shape[1] /2)
        template_height = int(img.shape[0] /2)
        dim = (template_width, template_height)

        img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
        cv.imshow("Resized image", img)
        cv.waitKey(0)

    hough_Transform(img)
    Search_Circle()
    Is_TemplateMatching()
    cropImage()
    BlopDetection()
    Get_Scores()


def hough_Transform(imgName):
    #Assign new image as cropted image
    if cropImg != "":   
        imgName = cropImg

    imgHs, imgWs = imgName.shape
    
    subtracts = 50
    max_radius = imgHs
    ranges = int(max_radius/subtracts)

    counter = 0
    for i in range(ranges):
        max_radius = max_radius - subtracts
        rows = imgName.shape[0]
        print(max_radius)
        circles = cv.HoughCircles(imgName, cv.HOUGH_GRADIENT, 1, rows / 8,
                                param1=100, param2=30,
                                minRadius=1, maxRadius=max_radius)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, 0:1]:   
                center = (i[0], i[1])
                radius = i[2]
                All_circle_radius.append(radius)
                print(radius)
                arrLen = len(All_circle_radius)
                firstRadius = All_circle_radius[arrLen - 2]                   
                RadiusDiffrence = abs(firstRadius - radius)
                print(RadiusDiffrence)    
                if ((RadiusDiffrence >= 0 and RadiusDiffrence <= 10)) and counter != 0:
                    continue
                else:
                    Selected_circle_radius.append(radius)
                    center_points.append(i[0])
                    center_points.append(i[1])
                    # circle center
                    if isTemplate == 1:
                        cv.circle(imgName, center, 1, (0, 100, 100), 3)
                    # circle outline
                    cv.circle(imgName, center, radius, (255, 0, 255), 3)
                    print(center)
                    cv.imshow("detected circles", imgName)
                    cv.waitKey(0)
                    counter = 1

def template_Matching(TemplateImg, TargetImg, Counter):
    global cropImg, template_scale_percent, isTemplate
    target_scale_percent1 = 100
    isTemplate = 1
    
    #Template scaling
    template_scale_percent = template_scale_percent - 10
    template_width = int(TemplateImg.shape[1] * (template_scale_percent / 100))
    template_height = int(TemplateImg.shape[0] * (template_scale_percent / 100))
    dim = (template_width, template_height)

    resizeds = cv.resize(TemplateImg, dim, interpolation = cv.INTER_AREA)
    cv.imshow("Resized image", resizeds)
    cv.waitKey(0)

    #Targer Scaling
    # scale_percent1 = scale_percent1 - 10
    target_width = int(TargetImg.shape[1] * (target_scale_percent1 / 100))
    target_height = int(TargetImg.shape[0] * (target_scale_percent1 / 100))
    dim1 = (target_width+20, target_height+20)

    target_scaled = cv.resize(TargetImg, dim1, interpolation = cv.INTER_AREA)
    # cv.imshow("Resized image", target_scaled)
    # cv.waitKey(0)
    print(target_width, target_height)

    # template.resize((template_height, template_width))
    h, w = TemplateImg.shape
    print(template_width, template_height)

    #Template Matching
    meth = "cv.TM_SQDIFF_NORMED"

    method = eval(meth)
    color = (0, 0, 0)

    try:
        # Apply template Matching
        res = cv.matchTemplate(target_scaled,resizeds,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # circle properties
        midx = (top_left[0] + bottom_right[0])//2
        midy = (top_left[1] + bottom_right[1])//2
        center_coordinates = midx, midy
        print(midx, midy)
        radius = int(math.sqrt((top_left[0]-midx)**2+(top_left[1]-midy)**2)/math.sqrt(2))

        cv.rectangle(target_scaled,top_left, bottom_right, color, 2)
        # cv.circle(target_scaled, center_coordinates, radius, color, 2)

        #Cropted Image
        rectX = midx - radius
        rectY = midy - radius
        cropImg = target_scaled[rectY:(rectY+2*radius), rectX:(rectX+2*radius)]
        # cropImg = cv.rectangle(target_scaled,top_left, bottom_right, color, 2)
        plt.imshow(cropImg,cmap = 'gray')
        plt.show()
    except:
        print("")


def Search_Circle():
    global try_templateMatching
    #Select the close radius that are similar between circles. If it is between +20 and -20 than it is in the same line.
    counter = 0
    for x in range(len(Selected_circle_radius)):
        counter = counter + 1
        for i in range(counter, len(Selected_circle_radius)):
            test = Selected_circle_radius[x] + 20
            test1 = Selected_circle_radius[x] - 20
            if Selected_circle_radius[i] > test1 and Selected_circle_radius[i] < test:
                # print("asd", Selected_circle_radius[i])
                Removed_Circle_radius_points.append(Selected_circle_radius[i])
                Removed_Circle_radius_points.append(i)

    #Select the duplicate ones
    [updated_Circle_radius_points.append(x) for x in Removed_Circle_radius_points if x not in updated_Circle_radius_points]

    #Check if there are duplicate radius numbers
    if not updated_Circle_radius_points:
        print("No duplicate radius")
    else:
        print("Duplicate radius:", updated_Circle_radius_points)

        #Remove the selected duplicate radius from the array
        for i in range(0,len(updated_Circle_radius_points),2):
            Selected_circle_radius.remove(updated_Circle_radius_points[i])

        print(Selected_circle_radius)

        #Select the center point that we remove radius and add them to array
        for i in range(1,len(updated_Circle_radius_points),2):
            Circle_locations.append(updated_Circle_radius_points[i]+updated_Circle_radius_points[i])
            Circle_locations.append(updated_Circle_radius_points[i]+updated_Circle_radius_points[i] + 1)

        #List the array from min to max
        Circle_locations.sort()
        print(Circle_locations)

        #Select the correct index numbers to remove from array
        # 2 3 6 7 = 2 2 4 4 
        first_Num = Circle_locations[0]
        Removed_Center_Points.append(first_Num)
        countss = 0

        for i in range(1, len(Circle_locations)):
            if first_Num + i == Circle_locations[i]:
                Removed_Center_Points.append(first_Num)
            else:
                numss = Circle_locations[i] - Circle_locations[i - 2]

                if countss == 0:
                    Removed_Center_Points.append(numss)
                    # Removed_Center_Points.append(first_Num+i)
                    countss = countss + 1
                else:
                    Removed_Center_Points.append(numss)
                    # Removed_Center_Points.append(first_Num+i-1)
                    countss = 0

        print("Silinen noktalar",Removed_Center_Points)
        print("noktalar silinmeden ??nceki hali", center_points)
        #Remove the center point that we remove radius
        for i in range(len(Removed_Center_Points)):
            del center_points[Removed_Center_Points[i]]

    print(center_points)

    #Divide circle center points to 100 so that we can see similar numbers
    # 345 324 375 456 = 3 3 3 4
    for i in range(0, len(center_points), 2):
        center_points_x.append(int(center_points[i]/100))

    for i in range(1, len(center_points), 2):
        center_points_y.append(int(center_points[i]/100))

    #Count the same numbers in array
    print(center_points_x)
    print(center_points_y)
    my_dict_x = {i: center_points_x.count(i) for i  in center_points_x}
    my_dict_y = {i: center_points_y.count(i) for i  in center_points_y}

    print(my_dict_x)
    print(my_dict_y)

    numx = 0
    numy = 0
    for x, x_count in list(my_dict_x.items()):
        if x_count != 5 and x_count != 4:
            my_dict_x.pop(x)
        if x_count == 3:
            numx = x

    for y, y_count in list(my_dict_y.items()):
        if y_count != 5 and y_count != 4:
            my_dict_y.pop(y)
        if y_count == 3:
            numy = y

    print(my_dict_x)
    print(my_dict_y)

    check = 0
    check1 = 0
    #Remove the circle points and radius that are not in the same location by looking at x coordinate
    counter1 = 0
    check_y = True
    for x, x_count in list(my_dict_x.items()):
        key = x
        if x_count == 5:
            check = 1
            numx = x
        if x_count == 4:
            numx = x
        for i in range(0, len(center_points), 2):
            if int(center_points[i - counter1]/100) != key:
                del center_points[i-counter1]
                del center_points[i-counter1]
                
                counter1 = counter1 + 2
                try:
                    if i != 0:
                        del Selected_circle_radius[int(i/2)]
                except:
                    del Selected_circle_radius[int(i/2)-1]
                    continue

    #Remove the circle points and radius that are not in the same location by looking at y coordinate
    if check_y == True:                
        counter2 = 0
        for y, y_count in list(my_dict_y.items()):
            key = y
            if y_count == 5:
                check1 = 1
                numy = y
            if y_count == 4:
                numy = y
            for i in range(1, len(center_points), 2):
                if int(center_points[i - counter2]/100) != key:
                    del center_points[i-counter2-1]
                    del center_points[i-counter2-1]

                    counter2 = counter2 + 2
                    nums = i - 1
                    try:
                        if nums != 0:
                            del Selected_circle_radius[int(nums/2)]
                    except:
                        del Selected_circle_radius[int(nums/2)-1]
                        continue
    
    print("g??ncel1", Selected_circle_radius)
    print("g??ncel1", center_points)

    numx1 = 0
    numy1 = 0
    #Change center points that are close to each other 300, 400, 290, 390 = 300, 400, 300, 400
    # if len(my_dict_x) != 0:
    for i in range(0,len(center_points),2):
        if int(center_points[i]/100) == numx:
            numx1 = center_points[i]
            break

    for i in range(0,len(center_points),2):
        if int(center_points[i]/100) != numx:
            if abs(np.int16(numx1 - center_points[i])) < 15:
                center_points[i] = numx1

    # if len(my_dict_y) != 0:
    for i in range(1,len(center_points),2):
        if int(center_points[i]/100) == numy:
            numy1 = center_points[i]
            break

    for i in range(1,len(center_points),2):
        if int(center_points[i]/100) != numy:
            if abs(np.int16(numy1 - center_points[i])) < 15:
                center_points[i] = numy1

    #Add 5th circle if there is 4 circles
    print("g??ncel", Selected_circle_radius)
    print("g??ncel", center_points)
     
    AddCircle()

    center_points_x.clear()
    center_points_y.clear()                
    for i in range(0, len(center_points), 2):
        center_points_x.append(int(center_points[i]/100))

    for i in range(1, len(center_points), 2):
        center_points_y.append(int(center_points[i]/100))

    my_dict_x = {i: center_points_x.count(i) for i  in center_points_x}
    my_dict_y = {i: center_points_y.count(i) for i  in center_points_y}

    for x, x_count in list(my_dict_x.items()):
        if x_count == 5:
            check = 1

    for y, y_count in list(my_dict_y.items()):
        if y_count == 5:
            check1 = 1
    
    print(my_dict_x)
    print(my_dict_y)

    if check == 1 and check1 == 1:
        try_templateMatching = False

    print(Selected_circle_radius)
    print(center_points)


def AddCircle():
    center_points_x.clear()
    center_points_y.clear() 
    for i in range(0, len(center_points), 2):
        center_points_x.append(int(center_points[i]/100))

    for i in range(1, len(center_points), 2):
        center_points_y.append(int(center_points[i]/100))

    my_dict_x = {i: center_points_x.count(i) for i  in center_points_x}
    my_dict_y = {i: center_points_y.count(i) for i  in center_points_y}

    for x, x_count in list(my_dict_x.items()):
        key = x
        if x_count == 4:
            for i in range(0, len(center_points), 2):
                if int(center_points[i]/100) == key:
                    center_points.append(center_points[i])
                    center_points.append(center_points[i+1])
                    break

            Selected_circle_radius.sort()
            for i in range(len(Selected_circle_radius)):
                if (i+1) < len(Selected_circle_radius):
                    fark = abs(Selected_circle_radius[i + 1] - Selected_circle_radius[i])
                    farkList.append(fark)

            for i in range(len(farkList)):
                if (i+1) < len(farkList):
                    fark1 = abs(np.int16(farkList[i + 1] - farkList[i]))
                    farkList1.append(fark1)

            print(farkList)
            print(farkList1)

            fark2 = abs(np.int16(farkList1[1] - farkList1[0]))
            print("farks", fark2)
            basaEkle = False
            sonaEkle = False

            #If fark2 is less than 20 then we add radius to the begining of the list or to the end of the list.
            if fark2 < 20:
                if abs(np.int16(farkList[1] - farkList[0])) > 10  and abs(np.int16(farkList[1] - farkList[2])) > 10:
                    addNum = Selected_circle_radius[2] - farkList[0]
                    Selected_circle_radius.insert(2, addNum)
                else:
                    for i in range(len(Selected_circle_radius)):
                        if Selected_circle_radius[i] < 100:
                            sonaEkle = True
                            basaEkle = False
                            break
                        else:
                            basaEkle = True
                            sonaEkle = False

                    if basaEkle == True:
                        addNum = Selected_circle_radius[0] - farkList[0]
                        Selected_circle_radius.insert(0, addNum)
                    elif sonaEkle == True:
                        addNum = Selected_circle_radius[3] + farkList[2]
                        Selected_circle_radius.append(addNum)                  
            elif fark2 > 20:
                #Check which number is bigger in [0, 2]. Then check the numbers that cause this. Add the corresponding number to radius list.
                if farkList1[1] > farkList1[0]:
                    num1 = Selected_circle_radius[3] - Selected_circle_radius[2]
                    num2 = Selected_circle_radius[2] - Selected_circle_radius[1]
                    if num1 > num2:
                        addNum = Selected_circle_radius[3] - farkList[2]
                        Selected_circle_radius.insert(3, addNum)
                    elif num2 > num1:
                        addNum = Selected_circle_radius[2] - farkList[2]
                        Selected_circle_radius.insert(2, addNum)
                elif farkList1[0] > farkList1[1]:
                    num1 = Selected_circle_radius[2] - Selected_circle_radius[1]
                    num2 = Selected_circle_radius[1] - Selected_circle_radius[0]
                    if num1 > num2:
                        addNum = Selected_circle_radius[2] - farkList[1]
                        Selected_circle_radius.insert(2, addNum)
                    elif num2 > num1:
                        addNum = Selected_circle_radius[1] - farkList[1]
                        Selected_circle_radius.insert(1, addNum)                                                               


def Is_TemplateMatching():
    global isTemplate, done
    if try_templateMatching == True:
        isTemplate = 1
        All_circle_radius.clear()
        Selected_circle_radius.clear()
        Removed_Circle_radius_points.clear()
        center_points.clear()
        center_points_x.clear()
        center_points_y.clear()
        Removed_Center_Points.clear()
        Circle_locations.clear()
        updated_Circle_radius_points.clear()

        for try_templateMatching_count in range(1, 10):
            img = cv.imread(targetName,0)

            if img.shape[0] > 1000 and img.shape[1] > 1000:
                template_width = int(img.shape[1] /2)
                template_height = int(img.shape[0] /2)
                dim = (template_width, template_height)

                img = cv.resize(img, dim, interpolation = cv.INTER_AREA)

            template_Matching(template, img, try_templateMatching_count)
            try:
                hough_Transform(img)
            except:
                continue

            Search_Circle()
            if try_templateMatching == False:
                break
            if try_templateMatching_count == 9:
                done = False

            All_circle_radius.clear()
            Selected_circle_radius.clear()
            Removed_Circle_radius_points.clear()
            center_points.clear()
            center_points_x.clear()
            center_points_y.clear()
            Removed_Center_Points.clear()
            Circle_locations.clear()
            updated_Circle_radius_points.clear()

    if done == False:
        print("Take Picture Again!!")

def cropImage():
    global croptedImg, farkW, farkH
    max_radius = Selected_circle_radius[0]
    counterss = 0
    for i in range(1, len(Selected_circle_radius)):
        if Selected_circle_radius[i] > max_radius:
            max_radius = Selected_circle_radius[i]
            counterss = i

    max_center_points_x = 0
    max_center_points_y = 0
    for i in range(len(center_points)):
        if int(i/2) == counterss:
            max_center_points_x = center_points[i-1]
            max_center_points_y = center_points[i]

    print("max x",max_center_points_x)
    print("max y",max_center_points_y)
    print("max yar????ap",max_radius)

    rectX = abs(max_center_points_x + 10 - max_radius)
    rectY = abs(max_center_points_y - max_radius)

    print(rectX)
    print(rectY)

    # Crop Image To Find Blops 
    if isTemplate == 0:
        img = cv.imread(targetName,0)
        

        if img.shape[0] > 1000 and img.shape[1] > 1000:
            template_width = int(img.shape[1] /2)
            template_height = int(img.shape[0] /2)
            dim = (template_width, template_height)

            img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
            cv.imshow("Resized image", img)
            cv.waitKey(0)

        imgW, imgH = img.shape
        croptedImg = img[rectY:(rectY+2*max_radius), rectX:(rectX+2*max_radius)]
        cropW, cropH = croptedImg.shape
        
        farkW = abs(imgW - cropW)
        farkH = abs(imgH - cropH)
        print("farkw", farkW)
        print("farkH", farkH)

        plt.imshow(croptedImg)
        plt.show()
    else:
        if cropImg != "":
            templateW, templateH = cropImg.shape
            croptedImg = cropImg[rectY:(rectY+2*max_radius), rectX:(rectX+2*max_radius)]
        else:
            img = cv.imread(targetName,0)
        
            if img.shape[0] > 1000 and img.shape[1] > 1000:
                template_width = int(img.shape[1] /2)
                template_height = int(img.shape[0] /2)
                dim = (template_width, template_height)

                img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
                cv.imshow("Resized image", img)
                cv.waitKey(0)

            templateW, templateH = img.shape
            croptedImg = img[rectY:(rectY+2*max_radius), rectX:(rectX+2*max_radius)]
        
        cropW, cropH = croptedImg.shape

        farkW = abs(templateW - cropW)
        farkH = abs(templateH - cropH)

        plt.imshow(croptedImg)
        plt.show()

def ThresHolding():
    global thresh1
    #Threshold
    ret,thresh1 = cv.threshold(croptedImg,30,255,cv.THRESH_BINARY)
    plt.imshow(thresh1,cmap = 'gray')
    plt.show()

def AdaptiveThreshold(num1):
    global thresh1
    thresh1 = cv.adaptiveThreshold(croptedImg,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv.THRESH_BINARY,11,num1)#8, 2
    plt.imshow(thresh1,cmap = 'gray')
    plt.show()

def HistogramEqualization():
    global thresh1
    thresh1 = cv.equalizeHist(croptedImg)
    cv.imshow("Histogram",thresh1)
    cv.waitKey()

def closing():
    global thresh1
    kernel = np.ones((5, 5), np.uint8)
    thresh1 = cv.morphologyEx(thresh1, cv.MORPH_CLOSE, kernel)

def opening():
    global thresh1
    kernel = np.ones((5, 5), np.uint8)
    thresh1 = cv.morphologyEx(thresh1, cv.MORPH_OPEN, kernel)

def erode():
    global thresh1
    kernel = np.ones((5, 5), np.uint8)
    thresh1 = cv.erode(thresh1, kernel, iterations=1)

def dilation():
    global thresh1
    kernel = np.ones((5, 5), np.uint8)
    thresh1 = cv.dilate(thresh1, kernel, iterations=1)

def BlopDetection():
    #Blop Param
    params = cv.SimpleBlobDetector_Params()

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 80

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1
    
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.1

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    params.minThreshold = 10
    params.maxThreshold = 200

    #Blop Detection
    detector = cv.SimpleBlobDetector_create(params)
    keypoints = detector.detect(croptedImg)
    with_keypoints = cv.drawKeypoints(croptedImg, keypoints, np.array([]), (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imshow("KeyPoints", with_keypoints)
    cv.waitKey(0)
    plt.show()

    #Locations of points
    num_of_points = len(keypoints)
    for count in range(num_of_points):
        Scored_Points.append(int(keypoints[count].pt[0]))
        Scored_Points.append(int(keypoints[count].pt[1]))
        print(keypoints[count].pt)

    print(Scored_Points)

def Get_Scores():
    min_radius = Selected_circle_radius[0]
    counteris = 0
    for i in range(1, len(Selected_circle_radius)):
        if Selected_circle_radius[i] < min_radius:
            min_radius = Selected_circle_radius[i]
            counteris = i

    min_center_points_x = 0
    min_center_points_y = 0
    for i in range(len(center_points)):
        if int(i/2) == counteris:
            min_center_points_x = center_points[i-1]
            min_center_points_y = center_points[i]

    print(min_center_points_x)
    print(min_center_points_y)

    Selected_circle_radius.sort()
    print(Selected_circle_radius)
    print(Scored_Points)

    for i in range(0, len(Scored_Points), 2):

        point_radius_x = abs(min_center_points_x - (Scored_Points[i] + farkH -50))
        point_radius_y = abs(min_center_points_y - (Scored_Points[i + 1] + farkW -50))

        point_radius = math.sqrt(point_radius_x**2 + point_radius_y**2)

        print(point_radius)

        if point_radius <= Selected_circle_radius[0]:
            cv.putText(img = croptedImg, text="10", org=(Scored_Points[i], Scored_Points[i + 1]), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),thickness=1)
            cv.imshow("10 Score",croptedImg)
            cv.waitKey(0)
            plt.show()
        elif point_radius >= Selected_circle_radius[0] and point_radius <= Selected_circle_radius[1]:
            cv.putText(img = croptedImg, text="9", org=(Scored_Points[i], Scored_Points[i + 1]), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),thickness=1)
            cv.imshow("9 Score",croptedImg)
            cv.waitKey(0)
            plt.show()
        elif point_radius >= Selected_circle_radius[1] and point_radius <= Selected_circle_radius[2]:
            cv.putText(img = croptedImg, text="8", org=(Scored_Points[i], Scored_Points[i + 1]), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),thickness=1)
            cv.imshow("8 Score",croptedImg)
            cv.waitKey(0)
            plt.show()
        elif point_radius >= Selected_circle_radius[2] and point_radius <= Selected_circle_radius[3]:
            cv.putText(img = croptedImg, text="7", org=(Scored_Points[i], Scored_Points[i + 1]), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),thickness=1)
            cv.imshow("7 Score",croptedImg)
            cv.waitKey(0)
            plt.show()
        elif point_radius >= Selected_circle_radius[3] and point_radius <= Selected_circle_radius[4]:
            cv.putText(img = croptedImg, text="6", org=(Scored_Points[i], Scored_Points[i + 1]), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),thickness=1)
            cv.imshow("6 Score",croptedImg)
            cv.waitKey(0)
            plt.show()
        else:
            continue
            # cv.putText(img = croptedImg, text="0", org=(Scored_Points[i], Scored_Points[i + 1]), fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255, 0, 0),thickness=1)
            # cv.imshow("0 Score",croptedImg)
            # cv.waitKey(0)
            # plt.show()

main()