%Get the neighbors of this cell we are allowed to visit
%Map: 2D Matrix where 1 represents a free cell and 0 a filled cell
%pos: [row, col] position we are in
%conn: Connectivity 4 or 8
function [neighbors] = GetNeighbors(map, pos, conn)

[rows cols] = size(map);    
neighbors = zeros(8);
%left
if pos(1) > 1 && map(pos(1)-1, pos(2)) == 1
   neighbors(1) = sub2ind([rows cols], pos(1)-1, pos(2));
end
%right
if pos(1) < rows && map(pos(1)+1, pos(2)) == 1
   neighbors(2) = sub2ind([rows cols], pos(1)+1, pos(2));
end
%up
if pos(2) > 1 && map(pos(1), pos(2) - 1) == 1
   neighbors(3) = sub2ind([rows cols], pos(1), pos(2) - 1);
end
%down
if pos(2) < cols && map(pos(1), pos(2) + 1) == 1
   neighbors(4) = sub2ind([rows cols], pos(1), pos(2) +1);
end

if conn == 8
    %top left
    if pos(1) > 1  && pos(2) > 1 && map(pos(1)-1, pos(2) - 1) == 1
        neighbors(5) = sub2ind([rows cols], pos(1)-1, pos(2)-1);
    end
    %bottom right
    if pos(1) < rows  && pos(2) < cols && map(pos(1)+1, pos(2) +1) == 1
        neighbors(6) = sub2ind([rows cols], pos(1)+1, pos(2)+1);
    end
    %bottom left
    if pos(1) < rows  && pos(2) > 1 && map(pos(1)+1, pos(2) -1) == 1
        neighbors(7) = sub2ind([rows cols], pos(1)+1, pos(2)-1);
    end
    %top right
    if pos(1) > 1  && pos(2) < cols && map(pos(1)-1, pos(2) +1) == 1
        neighbors(8) = sub2ind([rows cols], pos(1)-1, pos(2) + 1);
    end
end
