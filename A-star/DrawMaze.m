%map is a 2D matrix
%elements are defined as 1 = free, 0 = occupied
%note that cells are plotted as shifted by 0.5 to line up with grid lines
function [] = DrawMaze(map)
map = map';
[r,c] = size(map);                          %# Get the matrix size
imagesc((1:c)+0.5,(1:r)+0.5,map)            %# Plot the image
colormap(gray);                             %# Use a gray colormap
axis equal                                  %# Make axes grid sizes equal
set(gca,'XTick',1:(c+1),'YTick',1:(r+1),...   %# Change some axes properties
        'XLim',[1 c+1],'YLim',[1 r+1],...
        'GridLineStyle','-','XGrid','on','YGrid','on');
