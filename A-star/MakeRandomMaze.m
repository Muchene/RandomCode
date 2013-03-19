%width and length are integers
%obs_density is the probability of a cell being occupied (between 0 and 1)
function map = MakeRandomMaze(width,length,obs_density)

randnums = rand(width,length);
map = ones(width,length);
map(randnums(:) < obs_density) = 0;


