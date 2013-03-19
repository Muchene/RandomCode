clear all;
close all;

%define problem
width = 30;
length = 50;
obs_density = 0.5; %probabilit of a cell being an obstacle

%make map and make a start and goal
map = MakeRandomMaze(width,length,obs_density);
startind = find(map(:) == 1, 1, 'first');
goalind = find(map(:) == 1, 1, 'last');


%draw the maze as a black and white grid
DrawMaze(map);

%plot start and goal
[startsubx,startsuby] = ind2sub(size(map),startind);
[goalsubx,goalsuby] = ind2sub(size(map),goalind);
hold on;
plot(startsubx+0.5, startsuby+0.5,'r.')
plot(goalsubx+0.5, goalsuby+0.5,'g.')

Astar(map,startsubx,startsubx, goalsubx, goalsuby, 8, 2);