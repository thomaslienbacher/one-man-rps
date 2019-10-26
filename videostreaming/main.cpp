#include <iostream>
#include <thread>
#include <chrono>
#include <array>
#include <opencv2/opencv.hpp>

#define SSH_NO_CPP_EXCEPTIONS

#include <libssh/libsshpp.hpp>

int stream_camera() {
    cv::VideoCapture cv;

    auto conn = "tcp://raspberrypi:7799";

    if (cv.open(conn)) {//$ raspivid -t 9999999 -n -w 1280 -h 720 -fps 30 -ex fixedfps -b 3000000 -vf -o - | nc -l 7799
        cv::Mat mat;
        while (true) {
            cv >> mat;
            cv::imshow(conn, mat);
            if ((cv::waitKey(10) & 0xff) == 'q') break;
        }
    } else {
        std::cerr << "Can not open video source!";
        return 1;
    }

    return 0;
}

void print_usage() {
    printf("videostreaming (built on "
           __TIMESTAMP__
           ")\n"
           "Author: Thomas Lienbacher <lienbacher.tom@gmail.com>\n"
           "Displays the video stream from a Raspberry Pi Camera\n"
           "\n"
           "USAGE:\n"
           "    videostreaming <HOST> <PORT> <USERNAME> <PASSWORD>\n"
           "\n"
           "PARAMETERS:\n"
           "    HOST          \n"
           "    PORT          \n"
           "    USERNAME      \n"
           "    PASSWORD      \n"
           "\n");
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        print_usage();
        return 1;
    }

    std::string host(argv[1]);
    int port = std::strtol(argv[2], nullptr, 10);
    std::string username(argv[3]);
    std::string password(argv[4]);

    ssh::Session session;
    session.setOption(SSH_OPTIONS_HOST, host.c_str());
    session.setOption(SSH_OPTIONS_PORT, port);
    session.setOption(SSH_OPTIONS_TIMEOUT, 2);
    /*
    session.setOption(SSH_OPTIONS_LOG_VERBOSITY, SSH_LOG_WARN);
    session.setOption(SSH_OPTIONS_KNOWNHOSTS, R"(C:\Users\Thomas Lienbacher\.ssh\known_hosts)");
    session.setOption(SSH_OPTIONS_GLOBAL_KNOWNHOSTS, R"(C:\Users\Thomas Lienbacher\.ssh\known_hosts)");
    */

    int result = session.connect();
    if (result != SSH_OK) {
        std::cerr << "Error connecting: [" << session.getErrorCode() << "] " << session.getError() << std::endl;
        return 1;
    }

    session.setOption(SSH_OPTIONS_USER, username.c_str());
    result = session.userauthPassword(password.c_str());
    if (result != SSH_AUTH_SUCCESS) {
        std::cerr << "Couldn't authenticate!" << std::endl;
        return 1;
    }

    ssh::Channel channel(session);
    result = channel.openSession();
    if (result != SSH_OK) {
        std::cerr << "Error connecting: [" << session.getErrorCode() << "] " << session.getError() << std::endl;
        return 1;
    }

    channel.requestExec("raspivid -t 9999999 -n -w 1280 -h 720 -fps 30 -o - | nc -l 7799");
    std::this_thread::sleep_for(std::chrono::seconds(1));

    /*int read = 0;
    do {
        std::array<char, 128> buffer{};
        read = channel.read(buffer.data(), buffer.size(), 1);
        std::string str(buffer.data(), read);
        std::cout << str;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    } while (read);*/

    return stream_camera();
}