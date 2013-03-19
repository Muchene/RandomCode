function [] = general_search(map,start_x,start_y, goal_x, goal_y, conn, dist, version)

mex pq_create.cpp; 
mex pq_push.cpp; 
mex pq_pop.cpp; 
mex pq_size.cpp; 
mex pq_top.cpp;
mex pq_delete.cpp;

INF = 9999999999; %don't know if Matlab has a infinity sentinal 
[rows cols] = size(map);
start_ind = sub2ind([rows cols], start_x, start_y);
goal_ind  = sub2ind([rows cols], goal_x, goal_y);
f_costs = zeros(rows,cols);
g_costs = zeros(rows,cols);
open = zeros(rows, cols); %use this to decide how to color each cells
from = zeros(rows,cols); %keep track of the path


%initialize the costs to infinity and every cell as closed (or not visited)
for i=1:rows
    for j=1:cols
        f_costs(i,j) = INF;
        open(i,j) = 0;
    end
end


q = pq_create(rows*cols); %maybe over allocating memory here
f_costs(start_x, start_y) = 0;
pq_push(q, start_ind, f_costs(start_x, start_y));
open(start_x,start_y) = 1;
from(start_x,start_y) = start_ind;

%Run while the Queue has nodes not visited
while pq_size(q) > 0
    %Grab the node with minimum cost
    [curr curr_cost] = pq_pop(q);
    [curr_x curr_y] = ind2sub([rows cols], curr);
    open(curr_x, curr_y) = -1; %Mark node as expanded
    
    
    if curr == goal_ind
     %if we get to the goal print the path
     hold on;
     i = curr_x;
     j = curr_y;
     PlotExpansion(open,start_ind,goal_ind);
     while from(i,j) ~= start_ind
       [fromsubx fromsuby] = ind2sub([rows cols], from(i,j));  
        h = plot(fromsubx+0.5, fromsuby+0.5,'m.');
        set(h, 'LineWidth', 30);

        i = fromsubx;
        j = fromsuby;
        
     end
     pq_delete(q);
     return;
    end
    
    neighbors = GetNeighbors(map, [curr_x curr_y], conn);
    for i=1: length(neighbors)
        if neighbors(i) ~= 0
            [neigh_x neigh_y] = ind2sub([rows cols], neighbors(i));
            
            if version == 1
                new_cost = g_costs(curr_x, curr_y); %breadth First search
            elseif version == 2
                new_cost = norm([goal_x goal_y] - [neigh_x neigh_y], dist); %best first search
            else
                new_cost = g_costs(curr_x, curr_y) + norm([goal_x goal_y] - [neigh_x neigh_y], dist);%g(n)+h(n)
            end
            if new_cost < f_costs(neigh_x, neigh_y)
                %if this neighbor has no been expanded yet
                if open(neigh_x, neigh_y) ~= -1
                    pq_push(q,neighbors(i), new_cost);
                    f_costs(neigh_x, neigh_y) = new_cost;
                    g_costs(neigh_x, neigh_y) = g_costs(curr_x,curr_y) +1;
                    from(neigh_x, neigh_y) = curr;
                    open(neigh_x, neigh_y) = 1;
                end
            end
        end
    end
end

disp('No Solution Found');
PlotExpansion(open, start_ind, goal_ind);
pq_delete(q);
end



%Plot blue and cyan points according to how the algorithm 
%expanded the nodes
function [] = PlotExpansion(open_list,start_ind, goal_ind)

[rows cols] = size(open_list);
for i=1:rows
    for j= 1:cols
        if open_list(i,j) == -1 && (sub2ind([rows cols],i,j) ~= start_ind && sub2ind([rows cols],i,j) ~= goal_ind) 
            plot(i+0.5, j+0.5,'b.');
        elseif open_list(i,j) == 1 && (sub2ind([rows cols],i,j) ~= start_ind && sub2ind([rows cols],i,j) ~= goal_ind)
             plot(i+0.5, j+0.5,'c.');    
        end
    end
end       

end

