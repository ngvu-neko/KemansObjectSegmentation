import pygame
from random import randint
import math
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy


def crete_text_render(string):
    return font.render(string, True, WHITE)

def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def draw_img_with_k_cluster(img_name):
    "draw img with n cluster "

    img = plt.imread(f"{img_name}")

    width = img.shape[0]
    height = img.shape[1]

    print(img)
    img = img.reshape(width*height,3)

    print(img.shape)

    kmeans = KMeans(n_clusters=4).fit(img)

    labels = kmeans.predict(img)
    clusters = kmeans.cluster_centers_

    print(labels)
    print(clusters)
    img_2 = numpy.zeros((width,height,3),dtype= numpy.uint8)
    index = 0
    for i in range(width):
        for j in range(height):
            label_of_pixel = labels[index]
            img_2[i][j] = clusters[label_of_pixel]
            index +=1


    plt.imshow(img_2)
    plt.show()

WHITE  = (255, 255, 255)
BLACK = (0 , 0, 0)
BACKGROUND = (245,255,250)
GREEN = (140, 26, 255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)


#Set up screen of Kmeans
pygame.init()
screen = pygame.display.set_mode((1200,700))
pygame.display.set_caption("Kmeans Algorithm")


COLORS = [RED,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]
font = pygame.font.SysFont('sans', 27)
font_plus_mup = pygame.font.SysFont('sans',15)
text_random,text_run,text_alg,text_reset = crete_text_render("Random"),crete_text_render("Run"),\
                                           crete_text_render("Algorithm"),crete_text_render("Reset")
text_plus = font_plus_mup.render('+',True, WHITE)
text_mup = font_plus_mup.render('-',True, WHITE)


clock =  pygame.time.Clock()
running = True
K = 0
ERORR = 0
points = []
labels = []
clusters = []
active = False
ok_button_active = False
text = ''
while running:
    clock.tick(60)
    screen.fill(WHITE)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #draw panel
    pygame.draw.rect(screen, (240, 240, 240), (25, 25, 1150, 600))

    #k value
    k_value = font.render("K = "+ str(K), True,BLACK)
    screen.blit(k_value,(30,650))

    # Button +
    pygame.draw.rect(screen, GREEN, (125,645,20,20),border_radius=3)
    screen.blit(text_plus, (132,646))

    #button -
    pygame.draw.rect(screen, GREEN, (125,675,20,20),border_radius=3)
    screen.blit(text_mup, (132,674))


    #random Button
    pygame.draw.rect(screen, GREEN, (380,642,150,50),border_radius=3)
    screen.blit(text_random, (410,650))

    #run button
    pygame.draw.rect(screen,GREEN,(560,642,150,50),border_radius=3)
    screen.blit(text_run,(615,650))

    #alo button

    pygame.draw.rect(screen,GREEN,(740,642,150,50),border_radius=3)
    screen.blit(text_alg,(770,650))

    #Reset button
    pygame.draw.rect(screen,GREEN,(920,642,150,50),border_radius=3)
    screen.blit(text_reset,(965,650))

    input_box = pygame.draw.rect(screen,GREEN,(1100,642,90,50 ),border_radius=3)

    ok_box= pygame.draw.rect(screen,GREEN,(1160,625,15,15),border_radius=3)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            #Create point on panel
            if 25 < mouse_x < 1175 and 25< mouse_y< 625:
                labels = []
                point = [mouse_x-25,mouse_y-25]
                points.append(point)
            # K button +
            if 125 < mouse_x < 145 and 645 < mouse_y < 665:
                if K < 8:
                    K+=1

            #K button -
            if 125 < mouse_x < 145 and 675 < mouse_y < 695:
                if K >0:
                    K-=1

            #random button
            if 380 < mouse_x < 530 and 642 < mouse_y < 692:
                clusters = []
                labels = []
                for i in range(K):
                    random_point = [randint(0,1150),randint(0,600)]
                    clusters.append(random_point)
            #Run button
            if 560 < mouse_x < 710 and 642 < mouse_y < 692:
                labels = []

                if clusters ==[]:
                    continue
                #Assign points to closest cluster
                for p in points:
                    distances_to_cluster = []
                    for c in clusters:
                        dis = distance(p,c)
                        distances_to_cluster.append(dis)
                    label = distances_to_cluster.index(min(distances_to_cluster))
                    labels.append(label)

                #Update Cluseter
                for i in range(K):
                    sumx = 0
                    sumy = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sumx += points[j][0]
                            sumy += points[j][1]
                            count +=1
                        if count != 0:
                            new_cluster_x = int(sumx / count)
                            new_cluster_y = int(sumy / count)
                            clusters[i] = [new_cluster_x, new_cluster_y]

            #aglorithm  button
            if 740 < mouse_x < 890 and 642 < mouse_y < 692:
                if  K == 0 or points == []:
                    continue
                else:
                    kmeans = KMeans(n_clusters = K ).fit(points)
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_


            #reset button
            if 920 < mouse_x < 1070 and 642 < mouse_y < 692:
                K = 0
                ERORR = 0
                points = []
                labels = []
                clusters = []

            if input_box.collidepoint(event.pos) :
                active = not active
            else:
                active = False
            #(1160,625,15,15)

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    print(text)
                else:
                    text += event.unicode
            if 1160 < mouse_x < 1175 and 625 < mouse_y < 640:
                ok_button_active = not ok_button_active


    #draw points
    for i in range(len(points)):
        pygame.draw.circle(screen,BLACK,(points[i][0]+25,points[i][1]+25),6)
        if labels ==[]:
            pygame.draw.circle(screen,WHITE,(points[i][0]+25,points[i][1]+25),5)
        else:
            pygame.draw.circle(screen,COLORS[labels[i]],(points[i][0]+25,points[i][1]+25),5)
    #draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen,COLORS[i],(clusters[i][0]+25, clusters[i][1]+ 25),10)

    # Erorr
    ERORR = 0
    if labels != [] and clusters != []:
        for i in range(len(points)):
            ERORR+= distance(points[i], clusters[labels[i]])
    text_er = font.render("Error = "+ str(int(ERORR)), True, BLACK)
    screen.blit(text_er, (170,650))

    txt_surface = font.render(text, True, WHITE)
    # Blit the text.
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, GREEN, input_box,2,border_radius= 3)


    #draw 'text'  image file by sklearn
    if text != '' and ok_button_active:
        draw_img_with_k_cluster(text)
        ok_button_active = False
    pygame.display.flip()
pygame.quit()




