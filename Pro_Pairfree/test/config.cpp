#include <string>
#include <nlohmann/json.hpp>
#include <fstream>

class Config {
public:
    std::string ip, ap_ip, domain_id;
    std::uint16_t listening_port, sending_port, ap_port;

    void loadFromFile(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            throw std::runtime_error("Unable to open file: " + filename);
        }

        nlohmann::json config_json;
        file >> config_json;

        ip = config_json.at("ip").get<std::string>();
        ap_ip = config_json.at("ap_ip").get<std::string>();
        listening_port = config_json.at("listening_port").get<std::uint16_t>();
        sending_port = config_json.at("sending_port").get<std::uint16_t>();
        ap_port = config_json.at("ap_port").get<std::uint16_t>();
        domain_id = config_json.at("domain_id").get<std::string>();
    }
};
