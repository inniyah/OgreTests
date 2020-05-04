/*
Copyright (c) 2007 Ilya Baran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

#include <Pinocchio/skeleton.h>
#include <Pinocchio/utils.h>
#include <Pinocchio/debugging.h>
#include <Pinocchio/attachment.h>
#include <Pinocchio/pinocchioApi.h>

#include <fstream>
#include <istream>
#include <string>
#include <vector>

using namespace Pinocchio;

struct ArgData {
    ArgData() :
    stopAtMesh(false), stopAfterCircles(false), skelScale(1.), noFit(false),
        skeleton(HumanSkeleton()), stiffness(1.),
        skelOutName(""), weightOutName(""), objOutName("")
    {
    }

    bool stopAtMesh;
    bool stopAfterCircles;
    std::string filename;
    Quaternion<> meshTransform;
    double skelScale;
    bool noFit;
    Skeleton skeleton;
    std::string skeletonname;
    double stiffness;
    std::string skelOutName;
    std::string weightOutName;
    std::string objOutName;
};

void printUsageAndExit() {
    std::cout << "Usage: AttachWeights filename.obj" << std::endl;
    std::cout << "              [-skel skelname] [-rot x y z deg]* [-scale s]" << std::endl;
    std::cout << "              [-meshonly | -mo] [-circlesonly | -co]" << std::endl;
    std::cout << "              [-fit] [-stiffness s]" << std::endl;
    std::cout << "              [-skelOut skelOutFile] [-weightOut weightOutFile]" << std::endl;
    std::cout << "              [-objOut objOutFile]" << std::endl;

    exit(0);
}

ArgData processArgs(const std::vector<std::string> &args) {
    ArgData out;
    int cur = 2;
    int num = args.size();
    if (num < 2) {
        printUsageAndExit();
    }

    out.filename = args[1];

    while (cur < num) {
        std::string curStr = args[cur++];

        if (curStr == std::string("-skel")) {
            if (cur == num) {
                std::cout << "No skeleton specified; ignoring." << std::endl;
                continue;
            }

            curStr = args[cur++];

            if (curStr == std::string("human")) {
                out.skeleton = HumanSkeleton();
            } else if(curStr == std::string("horse")) {
                out.skeleton = HorseSkeleton();
            } else if(curStr == std::string("quad")) {
                out.skeleton = QuadSkeleton();
            } else if(curStr == std::string("centaur")) {
                out.skeleton = CentaurSkeleton();
            } else {
                out.skeleton = Pinocchio::CsvFileSkeleton(curStr);
            }

            out.skeletonname = curStr;
            continue;
        }

        if (curStr == std::string("-rot")) {
            if (cur + 3 >= num) {
                std::cout << "Too few rotation arguments; exiting." << std::endl;
                printUsageAndExit();
            }

            double x, y, z, deg;
            sscanf(args[cur++].c_str(), "%lf", &x);
            sscanf(args[cur++].c_str(), "%lf", &y);
            sscanf(args[cur++].c_str(), "%lf", &z);
            sscanf(args[cur++].c_str(), "%lf", &deg);

            out.meshTransform = Quaternion<>(Vector3(x, y, z), deg * M_PI / 180.) * out.meshTransform;
            continue;
        }

        if (curStr == std::string("-scale")) {
            if(cur >= num) {
                std::cout << "No scale provided; exiting." << std::endl;
                printUsageAndExit();
            }
            sscanf(args[cur++].c_str(), "%lf", &out.skelScale);
            continue;
        }

        if (curStr == std::string("-meshonly") || curStr == std::string("-mo")) {
            out.stopAtMesh = true;
            continue;
        }

        if (curStr == std::string("-circlesonly") || curStr == std::string("-co")) {
            out.stopAfterCircles = true;
            continue;
        }

        if (curStr == std::string("-fit")) {
            out.noFit = false;
            continue;
        } else if (curStr == std::string("-nofit")) {
            out.noFit = true;
            continue;
        }

        if (curStr == std::string("-stiffness")) {
            if (cur >= num) {
                std::cout << "No stiffness provided; exiting." << std::endl;
                printUsageAndExit();
            }
            sscanf(args[cur++].c_str(), "%lf", &out.stiffness);
            continue;
        }

        if (curStr == std::string("-skelOut")) {
            if(cur == num) {
                std::cout << "No skeleton output specified; ignoring." << std::endl;
                continue;
            }
            curStr = args[cur++];
            out.skelOutName = curStr;
            continue;
        }

        if (curStr == std::string("-weightOut")) {
            if (cur == num) {
                std::cout << "No weight output specified; ignoring." << std::endl;
                continue;
            }
            curStr = args[cur++];
            out.weightOutName = curStr;
            continue;
        }

        std::cout << "Unrecognized option: " << curStr << std::endl;
        printUsageAndExit();
    }

    return out;
}


int process(const std::vector<std::string> &args) {
    ArgData a = processArgs(args);

    Debugging::setOutStream(std::cout);

    Mesh m(a.filename);

    if (m.vertices.size() == 0) {
        std::cout << "Error reading file.  Aborting." << std::endl;
        exit(0);
        return EXIT_FAILURE;
    }

    //~ m.dump();

    for (int i = 0; i < (int)m.vertices.size(); ++i) {
        m.vertices[i].pos = a.meshTransform * m.vertices[i].pos;
    }

    m.normalizeBoundingBox();
    m.computeVertexNormals();

    Skeleton given = a.skeleton;
    given.scale(a.skelScale * 0.7);

    if (a.stopAtMesh) { // if early bailout
        return EXIT_FAILURE;
    }

    PinocchioOutput o;
    // do everything
    if (!a.noFit) {
        o = autorig(given, m);
    } else { // skip the fitting step--assume the skeleton is already correct for the mesh
        TreeType *distanceField = constructDistanceField(m);
        VisTester<TreeType> *tester = new VisTester<TreeType>(distanceField);

        o.embedding = a.skeleton.fGraph().verts;
        for (int i = 0; i < (int)o.embedding.size(); ++i) {
            o.embedding[i] = m.toAdd + o.embedding[i] * m.scale;
        }

        o.attachment = new Attachment(m, a.skeleton, o.embedding, tester, a.stiffness);

        delete tester;
        delete distanceField;
    }

    if (o.embedding.size() == 0) {
        std::cout << "Error embedding" << std::endl;
        return EXIT_FAILURE;
    }

    //~ a.skeleton.dump();

    // output skeleton embedding
    for (int joint = 0; joint < (int)o.embedding.size(); ++joint) {
        o.embedding[joint] = (o.embedding[joint] - m.toAdd) / m.scale;
    }

    if (a.skelOutName.length()) {
        std::ofstream os(a.skelOutName.c_str());

        os << "\"BoneNum\",\"Bone\",\"ParentNum\",\"Parent\",\"X\",\"Y\",\"Z\"" << std::endl;

        for (int joint = 0; joint < (int)o.embedding.size(); ++joint) {
            int parent = a.skeleton.fPrev()[joint];
            os << joint << ",\"" << a.skeleton.getNameForJoint(joint) << "\","
                << parent << ",\"" << a.skeleton.getNameForJoint(parent) << "\","
                << o.embedding[joint][0] << ","
                << o.embedding[joint][1] << ","
                << o.embedding[joint][2] << std::endl;
        }
    }

    // output attachment
    if (a.weightOutName.length()) {
        std::ofstream astrm(a.weightOutName.c_str());

        for (int joint = 1; joint < (int)o.embedding.size(); ++joint) {
            if (joint > 1) astrm << ",";
            astrm << "\"" << a.skeleton.getNameForJoint(joint) << "\"";
        }
        astrm << std::endl;

        for (int vertex = 0; vertex < (int)m.vertices.size(); ++vertex) {
            Vector<double, -1> weights = o.attachment->getWeights(vertex);
            for (int j = 0; j < weights.size(); ++j) {
                if (j) astrm << ",";
                double d = floor(0.5 + weights[j] * 10000.) / 10000.;
                astrm << d;
            }
            astrm << std::endl;
        }
    }

    delete o.attachment;

    return EXIT_SUCCESS;
}


int main (int argc, const char * const * argv, const char * const * envp) {
    //~ Pinocchio::CsvFileSkeleton("skeletons/human.csv");

    std::vector<std::string> args;
    for (int i = 0; i < argc; ++i) {
        args.push_back(argv[i]);
    }
    return process(args);
}
