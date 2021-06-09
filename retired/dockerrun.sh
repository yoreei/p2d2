docker run -d \
  -it \
  --name p2d2 \
  --mount type=bind,source=/mnt/d/git/p2d2,target=/code \
 p2d2-image 
