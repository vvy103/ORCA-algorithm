#include "mission.h"
#include <fstream>
#include <algorithm>

Mission::Mission(std::string fileName, unsigned int agentsNum, unsigned int stepsTh, bool time, size_t timeTh, bool speedStop) 
{
    taskReader = new XMLReader(fileName);
    agents = vector<Agent *>();
    this->agentsNum = agentsNum;
    stepsTreshhold = stepsTh;
    isTimeBounded = time;
    timeTreshhold = timeTh;

    map = nullptr;
    options = nullptr;
    missionResult = Summary();
    resultsLog = std::unordered_map<int, std::pair<bool, int>>();
    resultsLog.reserve(agentsNum);

    #if FULL_LOG
        taskLogger = new XMLLogger(XMLLogger::GenerateLogFileName(fileName, agentsNum), fileName);
        stepsLog = std::unordered_map<int, std::vector<Point>>();
        stepsLog.reserve(agentsNum);

        goalsLog = std::unordered_map<int, std::vector<Point>>();
        goalsLog.reserve(agentsNum);
    #endif

    collisionsCount = 0;
    collisionsObstCount = 0;
    stepsCount = 0;

    #if MAPF_LOG
        auto found = fileName.find_last_of(".");
        string tmpPAR = fileName.erase(found);
        std::string piece = "_" + std::to_string(agentsNum);
        tmpPAR.insert(found, piece);

        MAPFLog = MAPFInstancesLogger(tmpPAR);
    #endif

    commonSpeedsBuffer = std::vector<std::list<float>>(agentsNum, std::list<float>(COMMON_SPEED_BUFF_SIZE, 1.0));
    allStops = false;
    stopByMeanSpeed = speedStop;
}


Mission::Mission(const Mission &obj) 
{
    #if MAPF_LOG
        MAPFLog = obj.MAPFLog;
    #endif
    
    agents = obj.agents;
    map = obj.map;
    options = obj.options;
    missionResult = obj.missionResult;
    resultsLog = obj.resultsLog;
    collisionsCount = obj.collisionsCount;
    collisionsObstCount = obj.collisionsObstCount;
    stepsCount = obj.stepsCount;
    taskReader = (obj.taskReader == nullptr) ? nullptr : obj.taskReader->Clone();

    #if FULL_LOG
        taskLogger = (obj.taskLogger == nullptr) ? nullptr : obj.taskLogger->Clone();
        stepsLog = obj.stepsLog;
        goalsLog = obj.goalsLog;
    #endif
    commonSpeedsBuffer = obj.commonSpeedsBuffer;
    allStops = obj.allStops;
    stopByMeanSpeed = obj.stopByMeanSpeed;
}


Mission::~Mission() 
{
    for (auto &agent: agents) {
        if (agent != nullptr) {
            delete agent;
            agent = nullptr;
        }
    }

    if (map != nullptr) {
        delete map;
        map = nullptr;
    }

    if (options != nullptr) {
        delete options;
        options = nullptr;
    }

    if (taskReader != nullptr) {
        delete taskReader;
        taskReader = nullptr;
    }

    #if FULL_LOG
        if (taskLogger != nullptr) {
            delete taskLogger;
            taskLogger = nullptr;
        }
    #endif
}


bool Mission::ReadTask() 
{
    return taskReader->ReadData() && taskReader->GetMap(&map) && taskReader->GetAgents(agents, this->agentsNum) && taskReader->GetEnvironmentOptions(&options);
}


Summary Mission::StartMission() 
{
    SaveMapToDotMap("my_map.map");

    #if FULL_OUTPUT
        std::cout << "Start\n";
    #endif

    auto startpnt = std::chrono::high_resolution_clock::now();
    for (auto agent: agents) 
    {
        #if MAPF_LOG
            if (dynamic_cast<ORCAAgentWithPARAndECBS*>(agent) != nullptr) {
                dynamic_cast<ORCAAgentWithPARAndECBS *>(agent)->SetMAPFInstanceLoggerRef(&MAPFLog);
            }
        #endif

        bool found = agent->InitPath();
        #if FULL_OUTPUT
            if (!found) {
                std::cout << agent->GetID() << " " << "Path not found\n";
            }
        #endif
        resultsLog.insert({agent->GetID(), {false, 0}});

        #if FULL_LOG
            stepsLog.insert({agent->GetID(), std::vector<Point>()});
            stepsLog[agent->GetID()].push_back({agent->GetPosition()});
            goalsLog[agent->GetID()].push_back(agent->GetPosition());
        #endif

    }
    bool needToStop, needToStopByTime, needToStopBySteps, needToStopBySpeed;
    do {
        AssignNeighbours();

        for (auto &agent: agents) {
            agent->UpdatePrefVelocity();
        }

        for (auto &agent: agents) {
            agent->ComputeNewVelocity();
        }

        UpdateSate();
        auto checkpnt = std::chrono::high_resolution_clock::now();
        size_t nowtime = std::chrono::duration_cast<std::chrono::milliseconds>(checkpnt - startpnt).count();

        needToStopBySpeed = (stopByMeanSpeed and allStops);
        needToStopByTime = (isTimeBounded and nowtime >= timeTreshhold);
        needToStopBySteps = (!isTimeBounded and stepsCount >= stepsTreshhold);
        needToStop = needToStopBySpeed or needToStopByTime or needToStopBySteps;

    } while (!IsFinished() && !needToStop);

    auto endpnt = std::chrono::high_resolution_clock::now();
    size_t res = std::chrono::duration_cast<std::chrono::milliseconds>(endpnt - startpnt).count();

    float stepsSum = 0;
    float rate = 0;
    float MAPFTime = 0.0;
    int initCount = 0, uniCount = 0, updCount = 0, ECBSCount = 0, PARCount = 0, successCount = 0, unsuccessCount = 0, flowtimeMAPF = 0;

    for (auto &node: resultsLog) {

        if (!node.second.first) {
            node.second.second = stepsCount;
        }
        else {
            rate++;
        }
        stepsSum += node.second.second;
    }
    for (auto &agent: agents) {
        collisionsCount += agent->GetCollision().first;
        collisionsObstCount += agent->GetCollision().second;
        auto tmpPARAgent = dynamic_cast<agent_pnr *> (agent);
        if (tmpPARAgent != nullptr) {
            auto statMAPF = tmpPARAgent->GetMAPFStatistics();
            MAPFTime += statMAPF[CNS_MAPF_COMMON_TIME];
            initCount += static_cast<int>(statMAPF[CNS_MAPF_INIT_COUNT]);
            uniCount += static_cast<int>(statMAPF[CNS_MAPF_UNITE_COUNT]);
            updCount += static_cast<int>(statMAPF[CNS_MAPF_UPDATE_COUNT]);
            successCount += static_cast<int>(statMAPF[CNS_MAPF_SUCCESS_COUNT]);
            unsuccessCount += static_cast<int>(statMAPF[CNS_MAPF_UNSUCCESS_COUNT]);
            flowtimeMAPF += static_cast<int>(statMAPF[CNS_MAPF_FLOWTIME]);
        }
        else {
            auto tmpPARnECBSAgent = dynamic_cast<ORCAAgentWithPARAndECBS *> (agent);
            if (tmpPARnECBSAgent != nullptr) {
                auto statMAPF = tmpPARnECBSAgent->GetMAPFStatistics();
                MAPFTime += statMAPF[CNS_MAPF_COMMON_TIME];
                initCount += static_cast<int>(statMAPF[CNS_MAPF_INIT_COUNT]);
                uniCount += static_cast<int>(statMAPF[CNS_MAPF_UNITE_COUNT]);
                updCount += static_cast<int>(statMAPF[CNS_MAPF_UPDATE_COUNT]);
                ECBSCount += static_cast<int>(statMAPF[CNS_MAPF_ECBS_COUNT]);
                PARCount += static_cast<int>(statMAPF[CNS_MAPF_PAR_COUNT]);
                successCount += static_cast<int>(statMAPF[CNS_MAPF_SUCCESS_COUNT]);
                unsuccessCount += static_cast<int>(statMAPF[CNS_MAPF_UNSUCCESS_COUNT]);
                flowtimeMAPF += static_cast<int>(statMAPF[CNS_MAPF_FLOWTIME]);
            }
        }
    }

    missionResult[CNS_SUM_SUCCESS_RATE] = std::to_string(rate * 100 / agentsNum);
    missionResult[CNS_SUM_RUN_TIME] = std::to_string(((float) res) / 1000);
    missionResult[CNS_SUM_COLLISIONS] = std::to_string(collisionsCount / 2);
    missionResult[CNS_SUM_FLOW_TIME] = std::to_string(stepsSum * options->timestep);
    missionResult[CNS_SUM_MAKESPAN] = std::to_string(stepsCount * options->timestep);
    missionResult[CNS_SUM_COLLISIONS_OBS] = std::to_string(collisionsObstCount);

    missionResult[CNS_SUM_MAPF_MEAN_TIME] = std::to_string(MAPFTime);
    missionResult[CNS_SUM_MAPF_INIT_COUNT] = std::to_string(initCount);
    missionResult[CNS_SUM_MAPF_UNITE_COUNT] = std::to_string(uniCount);
    missionResult[CNS_SUM_MAPF_UPDATE_COUNT] = std::to_string(updCount);

    missionResult[CNS_SUM_MAPF_ECBS_COUNT] = std::to_string(ECBSCount);
    missionResult[CNS_SUM_MAPF_PAR_COUNT] = std::to_string(PARCount);

    missionResult[CNS_SUM_MAPF_FLOWTIME] = std::to_string(flowtimeMAPF);
    missionResult[CNS_SUM_MAPF_SUCCESS_COUNT] = std::to_string(successCount);
    missionResult[CNS_SUM_MAPF_UNSUCCESS_COUNT] = std::to_string(unsuccessCount);

    // 保存路径用于可视化
    SavePathToTxt("paths.txt");

    #if FULL_OUTPUT
        std::cout << "End\n";
    #endif
    return missionResult;
}


#if FULL_LOG
bool Mission::SaveLog() 
{
    taskLogger->SetResults(stepsLog, goalsLog, resultsLog);
    taskLogger->SetSummary(missionResult);
    return taskLogger->GenerateLog() && (stepsCount > 0);
}
#endif


void Mission::UpdateSate() 
{
    size_t i = 0;
    allStops = true;

    for (auto &agent: agents) {
        agent->ApplyNewVelocity();
        Point newPos = agent->GetPosition() + (agent->GetVelocity() * options->timestep);
        agent->SetPosition(newPos);
        commonSpeedsBuffer[i].pop_front();
        commonSpeedsBuffer[i].push_back(agent->GetVelocity().EuclideanNorm());

        float sum = 0.0f;
        float c = 0.0f;
        float y, t;
        float mean;
        for (auto speed: commonSpeedsBuffer[i]) {
            y = speed - c;
            t = sum + y;
            c = (t - sum) - y;
            sum = t;
        }
        mean = sum / commonSpeedsBuffer[i].size();

        if (mean >= MISSION_SMALL_SPEED) {
            allStops = false;
        }

        #if FULL_LOG
            stepsLog[agent->GetID()].push_back(newPos);
            goalsLog[agent->GetID()].push_back(agent->GetNext());
        #endif
        i++;
    }

    stepsCount++;
}


void Mission::AssignNeighbours() 
{
    for (auto &agent: agents) {
        for (auto &neighbour: agents) {
            if (agent != neighbour) {
                float distSq = (agent->GetPosition() - neighbour->GetPosition()).SquaredEuclideanNorm();
                agent->AddNeighbour(*neighbour, distSq);
            }
        }
        agent->UpdateNeighbourObst();
    }
}


bool Mission::IsFinished() 
{
    bool result = true;
    for (auto &agent: agents) {
        bool localres = agent->isFinished();
        resultsLog[agent->GetID()].first = agent->isFinished() && resultsLog[agent->GetID()].first;
        if (localres && !resultsLog[agent->GetID()].first) {
            resultsLog[agent->GetID()].first = true;
            resultsLog[agent->GetID()].second = stepsCount;
        }
        result = result && localres;
    }

    return result;
}

Mission &Mission::operator=(const Mission &obj) 
{
    if (this != &obj) {
        stepsCount = obj.stepsCount;
        stepsTreshhold = obj.stepsTreshhold;
        agentsNum = obj.agentsNum;
        collisionsCount = obj.collisionsCount;
        collisionsObstCount = obj.collisionsObstCount;
        taskReader = obj.taskReader;
        missionResult = obj.missionResult;
        resultsLog = obj.resultsLog;
        #if MAPF_LOG
            MAPFLog = obj.MAPFLog;
        #endif

        vector<Agent *> tmpAgents = vector<Agent *>(obj.agents.size());
        for (int i = 0; i < obj.agents.size(); i++) {
            tmpAgents.push_back(obj.agents[i]->Clone());
        }

        for (auto &agent: agents) {
            delete agent;
        }

        agents = tmpAgents;

        if (map != nullptr) {
            delete map;
        }
        map = (obj.map == nullptr) ? nullptr : new Map(*obj.map);

        if (options != nullptr) {
            delete options;
        }
        options = (obj.options == nullptr) ? nullptr : new environment_options(*obj.options);

        if (taskReader != nullptr) {
            delete taskReader;
        }
        taskReader = (obj.taskReader == nullptr) ? nullptr : obj.taskReader->Clone();

        #if FULL_LOG
            if (taskLogger != nullptr) {
                delete taskLogger;
            }
            taskLogger = (obj.taskLogger == nullptr) ? nullptr : obj.taskLogger->Clone();
            stepsLog = obj.stepsLog;
            goalsLog = obj.goalsLog;
        #endif
        commonSpeedsBuffer = obj.commonSpeedsBuffer;
        allStops = obj.allStops;
        stopByMeanSpeed = obj.stopByMeanSpeed;
    }
    return *this;
}


void Mission::SavePathToTxt(std::string fileName) 
{
    #if FULL_LOG
    std::ofstream outFile(fileName);
    if (!outFile.is_open()) {
        std::cout << "Error: Could not open file " << fileName << " for writing." << std::endl;
        return;
    }

    // 计算最大路径长度 (Makespan) 用于补齐
    size_t max_path_size = 0;
    for (auto &entry : stepsLog) {
        if (entry.second.size() > max_path_size) {
            max_path_size = entry.second.size();
        }
    }

    // 输出 Agent 路径
    for (unsigned int i = 0; i < agentsNum; ++i) {
        if (stepsLog.find(i) != stepsLog.end()) {
            outFile << i << ":";
            const auto& path = stepsLog[i];
            
            for (size_t t = 0; t < max_path_size; t++) {
                // 如果当前时间步在路径范围内，取路径点；否则取最后一个点（补齐）
                Point p = (t < path.size()) ? path[t] : path.back();
                
                // 将浮点 Point 转换为网格 Node (Row, Col)
                Node n = map->GetClosestNode(p);
                
                // 关键修正：Visualizer 要求格式为 (x, y) 即 (Column, Row)
                // n.j 是 Width (Column), n.i 是 Height (Row)
                outFile << "(" << n.j << "," << n.i << "),";
            }
            outFile << "\n"; 
        }
    }

    outFile.close();
    std::cout << "Paths saved to " << fileName << " (with padding and coord swap)." << std::endl;
    #else
        std::cout << "Error: FULL_LOG is not enabled." << std::endl;
    #endif
}


void Mission::SaveMapToDotMap(std::string fileName) 
{
    if (map == nullptr) {
        std::cout << "Error: Map is not initialized." << std::endl;
        return;
    }

    std::ofstream outFile(fileName);
    if (!outFile.is_open()) {
        std::cout << "Error: Could not open file " << fileName << " for writing." << std::endl;
        return;
    }

    outFile << "type octile\n"; 
    outFile << "height " << map->GetHeight() << "\n";
    outFile << "width " << map->GetWidth() << "\n";
    outFile << "map\n";

    for (int i = 0; i < map->GetHeight(); ++i) {
        for (int j = 0; j < map->GetWidth(); ++j) {
            if (map->CellIsObstacle(i, j)) {
                outFile << "@"; 
            } else {
                outFile << "."; 
            }
        }
        outFile << "\n"; 
    }

    outFile.close();
    std::cout << "Map saved to " << fileName << std::endl;
}