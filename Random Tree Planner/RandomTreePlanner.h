/**
Implementation of a simple motion planner. The planner works by growing a tree in the following manner
Choses a random state in the state space, choose a random state in the tree, if 
we can make a motion from the tree state to the random state add the random state into the tree. With some
small probability we will sample the goal state and check whether we can make the transition. If we can, the solution
is found and we can backtrack to produce a path. This is a very dumb planner and is just meant to explore OMPL
**/

#include <ompl/base/Planner.h>
#include <ompl/geometric/PathGeometric.h>
// often useful headers:
#include <ompl/util/RandomNumbers.h>
#include <ompl/tools/config/SelfConfig.h>
#include <fstream>
#include <ompl/base/spaces/SE2StateSpace.h>
using namespace std;

namespace ob = ompl::base;
namespace ompl
{
    class RandomTreePlanner : public base::Planner
    {
    public:
        RandomTreePlanner(const base::SpaceInformationPtr &si) : base::Planner(si, "the planner's name")
        {
            // the specifications of this planner (ompl::base::PlannerSpecs)
            specs_.approximateSolutions = false;

            goalBias_ = .05;
            
        }
        virtual ~RandomTreePlanner(void)
        {
           for(int i=0; i < tree.size(); i++)
                delete(tree[i]);
        }
        virtual base::PlannerStatus solve(const base::PlannerTerminationCondition &ptc)
        {
            // make sure the planner is configured correctly; ompl::base::Planner::checkValidity
            // ensures that there is at least one input state and a ompl::base::Goal object specified
            checkValidity();
            // get a handle to the Goal from the ompl::base::ProblemDefinition member, pdef_
            base::Goal *goal = pdef_->getGoal().get();
            
            //Log file to use for plotting
            fstream fileStream;
            fileStream.open("sampled_points.txt", fstream::out);
            // get input states with PlannerInputStates helper, pis_
            while (const base::State *st = pis_.nextStart())
            {
                Motion *motion = new Motion(si_);
                si_->copyState(motion->state, st);
                tree.push_back(motion);
            }
            if(!sampler_)
                sampler_ = si_->allocStateSampler();
            // periodically check if ptc() returns true.
            // if it does, terminate planning.
            Motion *solution = NULL;
            Motion *rmotion   = new Motion(si_);
            base::State *rstate = rmotion->state;
            const base::State *gstate = pis_.nextGoal(ptc);
            while (ptc() == false)
            {
                //sample the goal with probability goalBias_
                if (rng_.uniform01() < goalBias_)
                    si_->copyState(rstate,gstate);
                else
                    sampler_->sampleUniform(rstate);
                
            
                
                
                //OMPL_INFORM("Sampled state!");
                Motion* treeMotion = tree[rng_.uniformInt(0, tree.size()-1)];
                base::State* treeState = treeMotion->state;
               
                //I'm assuming this checks whether straight line path exists
                if (si_->checkMotion(treeMotion->state, rstate))
                {
                    const ob::SE2StateSpace::StateType *SE2state = (rstate->as<ob::SE2StateSpace::StateType>());
                    fileStream <<(*SE2state).getX()<<','<< (*SE2state).getY() << endl;
                    /* create a motion */
                    Motion *motion = new Motion(si_);
                    si_->copyState(motion->state, rstate);
                    motion->parent = treeMotion;
                    tree.push_back(motion);
                    //OMPL_INFORM("Added Motion!");
                    double dist = 0.0;
                    bool sat = goal->isSatisfied(motion->state, &dist);
                    if (sat)
                    {
                        //OMPL_INFORM("Solution Found!");
                        solution = motion;
                        break;
                    }
                  
                }   
                
            }
            fileStream.close();
            bool solved = false;
            //backtrack the solution if found
            if(solution != NULL)
            {
                fileStream.open("path.txt", fstream::out);
                vector<Motion*> mpath;
                while(solution != NULL)
                {
                    //OMPL_INFORM("Backtracking!");
                    mpath.push_back(solution);
                    solution = solution->parent;
                }
                
                ompl::geometric::PathGeometric *path = new ompl::geometric::PathGeometric(si_);
                for(int i=mpath.size()-1; i>=0; i--){
                    path->append(mpath[i]->state);
                    const ob::SE2StateSpace::StateType *SE2state = (mpath[i]->state->as<ob::SE2StateSpace::StateType>());
                    fileStream <<(*SE2state).getX()<<','<< (*SE2state).getY() << endl;
                }
                fileStream.close();
                pdef_->addSolutionPath(base::PathPtr(path),false,0.0);
                solved = true;
            }
            // Return a value from the PlannerStatus enumeration.
            // See ompl::base::PlannerStatus for the possible return values
            return base::PlannerStatus(solved, false);
        }
        virtual void clear(void)
        {
            Planner::clear();
            sampler_.reset();
            // clear the data structures here
            
        }
        // optional, if additional setup/configuration is needed, the setup() method can be implemented
        virtual void setup(void)
        {
            Planner::setup();
            // perhaps attempt some auto-configuration
            ompl::tools::SelfConfig sc(si_, getName());
        }
        virtual void getPlannerData(base::PlannerData &data) const
        {
            // fill data with the states and edges that were created
            // in the exploration data structure
            // perhaps also fill control::PlannerData
        }
    protected:
        class Motion
        {
            public:
                Motion(void) : state(NULL), parent(NULL)
                {
                }
                Motion(const base::SpaceInformationPtr &si) : state(si->allocState()), parent(NULL)
                {}
                ~Motion(void)
                 {}
                base::State *state;
                Motion *parent;
       };
        float goalBias_;
        base::StateSamplerPtr  sampler_;
        RNG rng_;
        vector<Motion*> tree;
        
        
        
    };
    
    
    
 
}
