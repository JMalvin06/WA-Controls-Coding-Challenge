#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32_multi_array.hpp"

using namespace std::chrono_literals;
using std::placeholders::_1;


class MergeArrays : public rclcpp::Node
{
  public:
    MergeArrays() : Node("merge_arrays"), hasArray1(false), hasArray2(false){
      sub1 = this->create_subscription<std_msgs::msg::Int32MultiArray>(
        "/input/array1", 10, std::bind(&MergeArrays::callbackArray1, this, _1)
      );

      sub2 = this->create_subscription<std_msgs::msg::Int32MultiArray>(
        "/input/array2", 10, std::bind(&MergeArrays::callbackArray2, this, _1)
      );

      pub = this->create_publisher<std_msgs::msg::Int32MultiArray>(
        "/output/array", 10
      );
    }

  private:
    rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr sub1;
    rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr sub2;
    rclcpp::Publisher<std_msgs::msg::Int32MultiArray>::SharedPtr pub;

    std::vector<int> array1;
    std::vector<int> array2;
    bool hasArray1;
    bool hasArray2;

    void callbackArray1(const std_msgs::msg::Int32MultiArray & msg){
      array1 = msg.data;
      hasArray1 = true;

      // only call if has both arrays
      if(hasArray2){
        publishConcat();
      }
    }

    void callbackArray2(const std_msgs::msg::Int32MultiArray & msg){
      array2 = msg.data;
      hasArray2 = true;

      // only call if has both arrays
      if(hasArray1){
        publishConcat();
      }
    }

    void publishConcat(){
      std::vector<int> concatArray = array1;
      concatArray.insert(concatArray.end(), array2.begin(), array2.end());

      // create a printable version of array
      std::string s;
      for(int num : concatArray){
        s += std::to_string(num) + " ";
      }

      std_msgs::msg::Int32MultiArray msg;
      msg.data = concatArray;

      pub->publish(msg);
      RCLCPP_INFO(this->get_logger(), "Published array: '%s' to /output/array", s.c_str());
    }
};

int main(int argc, char ** argv)
{
  (void) argc;
  (void) argv;
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MergeArrays>());
  rclcpp::shutdown();
  return 0;
}
