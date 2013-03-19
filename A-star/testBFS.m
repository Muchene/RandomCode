clear all;
close all;

%define problem
width = 30;
length = 50;
obs_density = 0.25; %probabilit of a cell being an obstacle

%make map and make a start and goal
%map = MakeRandomMaze(width,length,obs_density);
map = ones(width,length);
map(2:width,length-1) = 0;
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

%Astar_a(map,startsubx,startsubx, goalsubx, goalsuby);

%Astar_b(map,startsubx,startsubx, goalsubx, goalsuby);
%Astar_c(map,startsubx,startsubx, goalsubx, goalsuby);
%%Astar_d(map,startsubx,startsubx, goalsubx, goalsuby);
%BestFirstSearch(map,startsubx,startsubx, goalsubx, goalsuby,4,1);
BreadthFirstSearch(map,startsubx,startsubx, goalsubx, goalsuby,4,1);