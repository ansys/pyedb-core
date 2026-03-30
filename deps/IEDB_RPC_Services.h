#pragma once

#include <vector>
#include <memory>
#include <string>

class IEDB_RPC_Services
{

public:

    virtual int Initialize() = 0;

    virtual bool ExecuteRpc(const std::string& serviceName,
                            const std::string& rpcName,
                            const std::string& serializedRequest,
                            std::string& serializedResponse,
                            std::string& errorMessage) = 0;
};
