# gpt_cpp_maker
Creates and automatically compiles C++ programs from natural language input using GPT

## Setup

* Install openai python package: `pip install openai`.
* [Generate a key](https://beta.openai.com/account/api-keys) for using openai API.
* Store this key in a separate file.

## Usage

``` bash
# Export the key as an environment variable
export GPT_API_KEY=$(cat <path/to/openai_key>)

# Invoke the script
python scripts/gpt_cpp_maker.py -sp <PATH/FOR/GENERATED/SOURCE/CODE> -f objects.cpp -p "Create a C++ program that creates two squares and three triangles that have unique names. Store them in a vector and print out their names. All shapes inherit a common base class. Use shared pointers instead of raw pointers."
```

Output:
``` c++
========================
 C++ source code:
========================

#include <iostream>
#include <vector>
#include <memory>

class Shape {
public:
    virtual void printName() = 0;
};

class Triangle : public Shape {
public:
    Triangle(std::string name) : name(name) {}
    void printName() override {
        std::cout << "I am a triangle named " << name << std::endl;
    }
private:
    std::string name;
};

class Square : public Shape {
public:
    Square(std::string name) : name(name) {}
    void printName() override {
        std::cout << "I am a square named " << name << std::endl;
    }
private:
    std::string name;
};

int main() {
    std::vector<std::shared_ptr<Shape>> shapes;
    shapes.push_back(std::make_shared<Triangle>("triangle1"));
    shapes.push_back(std::make_shared<Triangle>("triangle2"));
    shapes.push_back(std::make_shared<Triangle>("triangle3"));
    shapes.push_back(std::make_shared<Square>("square1"));
    shapes.push_back(std::make_shared<Square>("square2"));

    for (auto& shape : shapes) {
        shape->printName();
    }

    return 0;
}

========================
 g++ compiler command:
========================

g++ -o objects objects.cpp
C++ program created.
```
