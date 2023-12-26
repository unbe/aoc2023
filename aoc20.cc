#include <iostream>
#include <list>
#include <string>
#include <variant>
#include <ranges>

#include <absl/strings/str_split.h>

int main() {
    typedef struct {
        char type;
        std::vector<std::string> dests;
    } node_t;
    std::unordered_map<std::string, node_t> nodes;
    for (std::string line; std::getline(std::cin, line);) {
        std::vector<std::string> dests = absl::StrSplit(line, absl::ByAnyChar(" ,->"), absl::SkipEmpty());
        std::string src = dests[0];
        dests.erase(dests.begin());
        nodes[src.substr(1)] = {src.at(0), dests};
    }
    std::map<std::string, bool> flip_state;
    std::unordered_map<std::string, std::unordered_map<std::string, bool>> nand_state;
    for (auto const& [name, node] : nodes) {
        if (node.type == '%') {
            flip_state[name] = false;
        }
        for(const auto& dest_name : node.dests) {
            auto& dest = nodes[dest_name];
            if (dest.type == '&') {
                nand_state[dest_name][name] = false;
            }
        }
    }
    typedef struct {
        std::string from;
        std::string to;
        bool high;
    } pulse_t;
    std::list<pulse_t> pulses;
    int lowcnt = 0;
    int highcnt = 0;
    std::vector<std::string> bits = {"mz"};
    for (int i = 0; i < 10000; i++) {
        pulses.push_back({"utton", "roadcaster", false});
        while(pulses.size() > 0) {
            auto pulse = pulses.front();
            pulses.pop_front();
            const auto& name = pulse.to;
            if (pulse.high) {
                highcnt++;
            } else {
                lowcnt++;
            }
            if (name == "output") {
                continue;
            }
            // part2 solved via input analysis for now. Need to think how a generic solution 
            // would look like.
            if (name == "rx" || name == "fn"  || name == "hh" || name == "fh" || name == "lk") {
                if (!pulse.high) {
                    std::cout << "part2: " << name << ": " << (i + 1) << std::endl;
                }
                continue;
            }
            assert(nodes.count(name) == 1);
            const auto& node = nodes[name];
            switch(node.type) {
                case 'b': {
                    for (const auto& dest : node.dests) {
                        pulses.push_back({name, dest, pulse.high});
                    }
                    break;
                }
                case '&': {
                    auto* state = &nand_state[name];
                    nand_state[name][pulse.from] = pulse.high;
                    auto&& vals = std::views::values(*state);
                    bool high = !std::all_of(vals.begin(), vals.end(), std::identity()); 
                    for (const auto& dest : node.dests) {
                        pulses.push_back({pulse.to, dest, high});
                    }
                    break;
                }
                case '%': {
                    if (pulse.high) {
                        break;
                    }
                    bool high = flip_state[name] = !flip_state[name];
                    for (const auto& dest : node.dests) {
                        pulses.push_back({name, dest, high});
                    }
                    break;
                }
                default: {
                    std::cout << "Bad node type: " << node.type << "." << name << std::endl;
                    assert(false);
                }
            }
        }
        if (i == 999) {
            std::cout << "part1: " << static_cast<uint64_t>(highcnt)*lowcnt << std::endl;
        }
    }
};
