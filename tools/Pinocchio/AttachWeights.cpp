#include <Pinocchio/skeleton.h>
#include <Pinocchio/utils.h>
#include <Pinocchio/debugging.h>
#include <Pinocchio/attachment.h>
#include <Pinocchio/pinocchioApi.h>

#include <fstream>

using namespace Pinocchio;

struct ArgData {
    ArgData() :
    stopAtMesh(false), stopAfterCircles(false), skelScale(1.), noFit(true),
        skeleton(HumanSkeleton()), stiffness(1.),
        skelOutName("skeleton.out"), weightOutName("attachment.out")
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
};

void printUsageAndExit() {
    std::cout << "Usage: attachWeights filename.{obj | ply | off | gts | stl}" << std::endl;
    std::cout << "              [-skel skelname] [-rot x y z deg]* [-scale s]" << std::endl;
    std::cout << "              [-meshonly | -mo] [-circlesonly | -co]" << std::endl;
    std::cout << "              [-fit] [-stiffness s]" << std::endl;
    std::cout << "              [-skelOut skelOutFile] [-weightOut weightOutFile]" << std::endl;

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
                out.skeleton = FileSkeleton(curStr);
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


void process(const std::vector<std::string> &args) {
    int i;
    ArgData a = processArgs(args);

    Debugging::setOutStream(std::cout);

    Mesh m(a.filename);

    if (m.vertices.size() == 0) {
        std::cout << "Error reading file.  Aborting." << std::endl;
        exit(0);
        return;
    }

    for (i = 0; i < (int)m.vertices.size(); ++i) {
        m.vertices[i].pos = a.meshTransform * m.vertices[i].pos;
    }

    m.normalizeBoundingBox();
    m.computeVertexNormals();

    Skeleton given = a.skeleton;
    given.scale(a.skelScale * 0.7);

    // if early bailout
    if (a.stopAtMesh) {
        return;
    }

    PinocchioOutput o;
    // do everything
    if (!a.noFit) {
        o = autorig(given, m);
    } else { // skip the fitting step--assume the skeleton is already correct for the mesh
        TreeType *distanceField = constructDistanceField(m);
        VisTester<TreeType> *tester = new VisTester<TreeType>(distanceField);

        o.embedding = a.skeleton.fGraph().verts;
        for(i = 0; i < (int)o.embedding.size(); ++i)
            o.embedding[i] = m.toAdd + o.embedding[i] * m.scale;

        o.attachment = new Attachment(m, a.skeleton, o.embedding, tester, a.stiffness);

        delete tester;
        delete distanceField;
    }

    if (o.embedding.size() == 0) {
        std::cout << "Error embedding" << std::endl;
        exit(0);
    }

    // output skeleton embedding
    for(i = 0; i < (int)o.embedding.size(); ++i) {
        o.embedding[i] = (o.embedding[i] - m.toAdd) / m.scale;
    }
    std::ofstream os(a.skelOutName.c_str());
    for(i = 0; i < (int)o.embedding.size(); ++i) {
        os << i << " " << o.embedding[i][0] << " " << o.embedding[i][1] <<
            " " << o.embedding[i][2] << " " << a.skeleton.fPrev()[i] << std::endl;
    }

    // output attachment
    std::ofstream astrm(a.weightOutName.c_str());
    for (i = 0; i < (int)m.vertices.size(); ++i) {
        Vector<double, -1> v = o.attachment->getWeights(i);
        for (int j = 0; j < v.size(); ++j) {
            double d = floor(0.5 + v[j] * 10000.) / 10000.;
            astrm << d << " ";
        }
        astrm << std::endl;
    }

    delete o.attachment;
}


int main (int argc, const char * const * argv, const char * const * envp) {
    std::vector<std::string> args;
    for(int i = 0; i < argc; ++i) {
        args.push_back(argv[i]);
    }
    process(args);

    return EXIT_SUCCESS;
}
