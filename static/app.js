$(function(){
  background(89, 216, 255);
  var drawSeaWeed=function(x){
    noStroke();
    beginShape();

    curveVertex(x, 300);
    curveVertex(5*x, 20);
    curveVertex(300, 600);
    curveVertex(600, 2*x);
    endShape();
      };

  fill(100,355, 0);
  drawSeaWeed(36);
  fill(10,55, 100);
  drawSeaWeed(-3);
  fill(100,5, 0);
  drawSeaWeed(54);

  var drawFish=function(r,g,b, centerX, centerY, bodyLength, bodyHeight){
      noStroke();
      var bodyColor=color(r,g,b);
      fill(bodyColor);
      // body
      ellipse(centerX, centerY, bodyLength, bodyHeight);
      // tail
      var tailWidth = bodyLength/4;
      var tailHeight = bodyHeight/2;
      triangle(centerX-bodyLength/2, centerY,
               centerX-bodyLength/2-tailWidth, centerY-tailHeight,
               centerX-bodyLength/2-tailWidth, centerY+tailHeight);
      // eye
      fill(33, 33, 33);
      ellipse(centerX+bodyLength/4, centerY, bodyHeight/5, bodyHeight/5);

  };

  drawFish(250,0,230,100, 200, 80, 100);
  drawFish(200,0,30,50, 30, 60, 40);
  drawFish(20,100,30,40, 399, 50, 40);
  drawFish(150,250,20,200, 100, 30, 10);
  drawFish(50,0,230,210, 60, 120, 50);

  mouseClicked=function(){
    noStroke();
    var bodyColor=color(mouseX,mouseY,mouseX+mouseY);
    fill(bodyColor);
    ellipse(mouseX, mouseY, 40, 20);
    // tail
   var tailWidth = 40/4;
    var tailHeight = 20/2;
    triangle(mouseX-40/2, mouseY,
             mouseX-40/2-tailWidth, mouseY-tailHeight,
             mouseX-40/2-tailWidth, mouseY+tailHeight);
    // eye
    fill(33, 33, 33);
    ellipse(mouseX+40/4, mouseY, 20/5, 20/5);
  };
})
