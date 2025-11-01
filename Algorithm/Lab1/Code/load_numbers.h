//
// Created by 21035 on 2025/9/30.
//

#ifndef LAB1_LOAD_NUMBERS_H
#define LAB1_LOAD_NUMBERS_H

#include <fstream>
#include <vector>
#include <string>
#include "stdint.h"

std::vector<uint32_t> get_numbers_from_log(const std::string & filename);

#endif //LAB1_LOAD_NUMBERS_H