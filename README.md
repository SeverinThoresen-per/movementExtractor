# movementExtractor
A website an a flask server backend. Upload video files to the website, the video file is sent to the backend and returns a video file that consists entirely of "movement frames" and some statistical analysis about the movement.

Tasks : 

Website Layout Tasks : 

 - add a slider for the amount of changed pixels counting as movement

Server Tasks : 

 - send user traffic information to the server and store in an django
   database

Video Processing Tasks :

 - grayscale given videos
 - compress videos to have less pixels
 - identify "boxes" of changed pixels
 - draw up arrays of movement vectors for those boxes

Pong Tasks : 

 - use the arrays of movement vectors to create an algorithm for a 
   heatmap and other movement analytics
