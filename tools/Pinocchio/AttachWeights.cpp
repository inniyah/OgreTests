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

namespace Skeletons {

    // https://stackoverflow.com/questions/1120140/how-can-i-read-and-parse-csv-files-in-c

    enum class CSVState {
        UnquotedField,
        QuotedField,
        QuotedQuote
    };

    const std::string WHITESPACE = " \n\r\t\f\v";

    std::string ltrim(const std::string & s) {
        size_t start = s.find_first_not_of(WHITESPACE);
        return (start == std::string::npos) ? "" : s.substr(start);
    }

    std::string rtrim(const std::string & s) {
        size_t end = s.find_last_not_of(WHITESPACE);
        return (end == std::string::npos) ? "" : s.substr(0, end + 1);
    }

    std::string trim(const std::string & s) {
        return rtrim(ltrim(s));
    }

    std::vector<std::string> readCSVRow(const std::string &row) {
        CSVState state = CSVState::UnquotedField;

        const char *vinit[] = {""};
        std::vector<std::string> fields(vinit, std::end(vinit));

        size_t i = 0; // index of the current field
        for (char c : row) {
            switch (state) {
                case CSVState::UnquotedField:
                    switch (c) {
                        case ',': // end of field
                                  fields.push_back(""); i++;
                                  break;
                        case '"': state = CSVState::QuotedField;
                                  break;
                        default:  fields[i].push_back(c);
                                  break; }
                    break;
                case CSVState::QuotedField:
                    switch (c) {
                        case '"': state = CSVState::QuotedQuote;
                                  break;
                        default:  fields[i].push_back(c);
                                  break; }
                    break;
                case CSVState::QuotedQuote:
                    switch (c) {
                        case ',': // , after closing quote
                                  fields.push_back(""); i++;
                                  state = CSVState::UnquotedField;
                                  break;
                        case '"': // "" -> "
                                  fields[i].push_back('"');
                                  state = CSVState::QuotedField;
                                  break;
                        default:  // end of quote
                                  state = CSVState::UnquotedField;
                                  break; }
                    break;
            }
        }
        return fields;
    }

    /// Read CSV file, Excel dialect. Accept "quoted fields ""with quotes"""
    std::vector<std::vector<std::string>> readCSV(std::istream &in) {
        std::vector<std::vector<std::string>> table;
        std::string row;
        while (!in.eof()) {
            std::getline(in, row);
            if (in.bad() || in.fail()) {
                break;
            }
            row = trim(row);
            if (!row.length()) continue;
            auto fields = readCSVRow(row);
            table.push_back(fields);
        }
        return table;
    }

    struct Human : public ::Pinocchio::Skeleton {
        Human() {
            // Order of makeJoint calls is very important
            makeJoint("shoulders",  Vector3(0., 0.5, 0.));                     //0
            makeJoint("back",       Vector3(0., 0.15, 0.),      "shoulders");  //1
            makeJoint("hips",       Vector3(0., 0., 0.),        "back");       //2
            makeJoint("head",       Vector3(0., 0.7, 0.),       "shoulders");  //3

            makeJoint("lthigh",     Vector3(-0.1, 0., 0.),      "hips");       //4
            makeJoint("lknee",      Vector3(-0.15, -0.35, 0.),  "lthigh");     //5
            makeJoint("lankle",     Vector3(-0.15, -0.8, 0.),   "lknee");      //6
            makeJoint("lfoot",      Vector3(-0.15, -0.8, 0.1),  "lankle");     //7

            makeJoint("rthigh",     Vector3(0.1, 0., 0.),       "hips");       //8
            makeJoint("rknee",      Vector3(0.15, -0.35, 0.),   "rthigh");     //9
            makeJoint("rankle",     Vector3(0.15, -0.8, 0.),    "rknee");      //10
            makeJoint("rfoot",      Vector3(0.15, -0.8, 0.1),   "rankle");     //11

            makeJoint("lshoulder",  Vector3(-0.2, 0.5, 0.),     "shoulders");  //12
            makeJoint("lelbow",     Vector3(-0.4, 0.25, 0.075), "lshoulder");  //13
            makeJoint("lhand",      Vector3(-0.6, 0.0, 0.15),   "lelbow");     //14

            makeJoint("rshoulder",  Vector3(0.2, 0.5, 0.),      "shoulders");  //15
            makeJoint("relbow",     Vector3(0.4, 0.25, 0.075),  "rshoulder");  //16
            makeJoint("rhand",      Vector3(0.6, 0.0, 0.15),    "relbow");     //17

            // Symmetry
            makeSymmetric("lthigh", "rthigh");
            makeSymmetric("lknee", "rknee");
            makeSymmetric("lankle", "rankle");
            makeSymmetric("lfoot", "rfoot");

            makeSymmetric("lshoulder", "rshoulder");
            makeSymmetric("lelbow", "relbow");
            makeSymmetric("lhand", "rhand");

            initCompressed();

            setFoot("lfoot");
            setFoot("rfoot");

            setFat("hips");
            setFat("shoulders");
            setFat("head");
        }
    };


    struct Quad : public ::Pinocchio::Skeleton {
        Quad() {
            // Order of makeJoint calls is very important
            makeJoint("shoulders",  Vector3(0., 0., 0.5));                     //0
            makeJoint("back",       Vector3(0., 0., 0.),         "shoulders"); //1
            makeJoint("hips",       Vector3(0., 0., -0.5),       "back");      //2
            makeJoint("neck",       Vector3(0., 0.2, 0.63),      "shoulders"); //3
            makeJoint("head",       Vector3(0., 0.2, 0.9),       "neck");      //4

            makeJoint("lthigh",     Vector3(-0.15, 0., -0.5),    "hips");      //5
            makeJoint("lhknee",     Vector3(-0.2, -0.4, -0.5),   "lthigh");    //6
            makeJoint("lhfoot",     Vector3(-0.2, -0.8, -0.5),   "lhknee");    //7

            makeJoint("rthigh",     Vector3(0.15, 0., -0.5),     "hips");      //8
            makeJoint("rhknee",     Vector3(0.2, -0.4, -0.5),    "rthigh");    //9
            makeJoint("rhfoot",     Vector3(0.2, -0.8, -0.5),    "rhknee");    //10

            makeJoint("lshoulder",  Vector3(-0.2, 0., 0.5),      "shoulders"); //11
            makeJoint("lfknee",     Vector3(-0.2, -0.4, 0.5),    "lshoulder"); //12
            makeJoint("lffoot",      Vector3(-0.2, -0.8, 0.5),   "lfknee");    //13

            makeJoint("rshoulder",  Vector3(0.2, 0.0, 0.5),      "shoulders"); //14
            makeJoint("rfknee",     Vector3(0.2, -0.4, 0.5),     "rshoulder"); //15
            makeJoint("rffoot",      Vector3(0.2, -0.8, 0.5),    "rfknee");    //16

            makeJoint("tail",       Vector3(0., 0., -0.7),       "hips");      //17

            // Symmetry
            makeSymmetric("lthigh", "rthigh");
            makeSymmetric("lhknee", "rhknee");
            makeSymmetric("lhfoot", "rhfoot");

            makeSymmetric("lshoulder", "rshoulder");
            makeSymmetric("lfknee", "rfknee");
            makeSymmetric("lffoot", "rffoot");

            initCompressed();

            setFoot("lhfoot");
            setFoot("rhfoot");
            setFoot("lffoot");
            setFoot("rffoot");

            setFat("hips");
            setFat("shoulders");
            setFat("head");
        }
    };

    struct Horse : public ::Pinocchio::Skeleton {
        Horse() {
            // Order of makeJoint calls is very important
            makeJoint("shoulders",  Vector3(0., 0., 0.5));                     //0
            makeJoint("back",       Vector3(0., 0., 0.),         "shoulders"); //1
            makeJoint("hips",       Vector3(0., 0., -0.5),       "back");      //2
            makeJoint("neck",       Vector3(0., 0.2, 0.63),      "shoulders"); //3
            makeJoint("head",       Vector3(0., 0.2, 0.9),       "neck");      //4

            makeJoint("lthigh",     Vector3(-0.15, 0., -0.5),    "hips");      //5
            makeJoint("lhknee",     Vector3(-0.2, -0.2, -0.45),  "lthigh");    //6
            makeJoint("lhheel",     Vector3(-0.2, -0.4, -0.5),   "lhknee");    //7
            makeJoint("lhfoot",     Vector3(-0.2, -0.8, -0.5),   "lhheel");    //8

            makeJoint("rthigh",     Vector3(0.15, 0., -0.5),     "hips");      //9
            makeJoint("rhknee",     Vector3(0.2, -0.2, -0.45),   "rthigh");    //10
            makeJoint("rhheel",     Vector3(0.2, -0.4, -0.5),    "rhknee");    //11
            makeJoint("rhfoot",     Vector3(0.2, -0.8, -0.5),    "rhheel");    //12

            makeJoint("lshoulder",  Vector3(-0.2, 0., 0.5),      "shoulders"); //13
            makeJoint("lfknee",     Vector3(-0.2, -0.4, 0.5),    "lshoulder"); //14
            makeJoint("lffoot",      Vector3(-0.2, -0.8, 0.5),   "lfknee");    //15

            makeJoint("rshoulder",  Vector3(0.2, 0.0, 0.5),      "shoulders"); //16
            makeJoint("rfknee",     Vector3(0.2, -0.4, 0.5),     "rshoulder"); //17
            makeJoint("rffoot",      Vector3(0.2, -0.8, 0.5),    "rfknee");    //18

            makeJoint("tail",       Vector3(0., 0., -0.7),       "hips");      //19

            // Symmetry
            makeSymmetric("lthigh", "rthigh");
            makeSymmetric("lhknee", "rhknee");
            makeSymmetric("lhheel", "rhheel");
            makeSymmetric("lhfoot", "rhfoot");

            makeSymmetric("lshoulder", "rshoulder");
            makeSymmetric("lfknee", "rfknee");
            makeSymmetric("lffoot", "rffoot");

            initCompressed();

            setFoot("lhfoot");
            setFoot("rhfoot");
            setFoot("lffoot");
            setFoot("rffoot");

            setFat("hips");
            setFat("shoulders");
            setFat("head");
        }
    };

    struct Centaur : public ::Pinocchio::Skeleton {
        Centaur() {
            // Order of makeJoint calls is very important
            makeJoint("shoulders",  Vector3(0., 0., 0.5));                     //0
            makeJoint("back",       Vector3(0., 0., 0.),         "shoulders"); //1
            makeJoint("hips",       Vector3(0., 0., -0.5),       "back");      //2

            makeJoint("hback",      Vector3(0., 0.25, 0.5),      "shoulders"); //3
            makeJoint("hshoulders", Vector3(0., 0.5, 0.5),       "hback");     //4
            makeJoint("head",       Vector3(0., 0.7, 0.5),       "hshoulders");//5

            makeJoint("lthigh",     Vector3(-0.15, 0., -0.5),    "hips");      //6
            makeJoint("lhknee",     Vector3(-0.2, -0.4, -0.45),  "lthigh");    //7
            makeJoint("lhfoot",     Vector3(-0.2, -0.8, -0.5),   "lhknee");    //8

            makeJoint("rthigh",     Vector3(0.15, 0., -0.5),     "hips");      //9
            makeJoint("rhknee",     Vector3(0.2, -0.4, -0.45),   "rthigh");    //10
            makeJoint("rhfoot",     Vector3(0.2, -0.8, -0.5),    "rhknee");    //11

            makeJoint("lshoulder",  Vector3(-0.2, 0., 0.5),      "shoulders"); //12
            makeJoint("lfknee",     Vector3(-0.2, -0.4, 0.5),    "lshoulder"); //13
            makeJoint("lffoot",     Vector3(-0.2, -0.8, 0.5),    "lfknee");    //14

            makeJoint("rshoulder",  Vector3(0.2, 0.0, 0.5),      "shoulders"); //15
            makeJoint("rfknee",     Vector3(0.2, -0.4, 0.5),     "rshoulder"); //16
            makeJoint("rffoot",     Vector3(0.2, -0.8, 0.5),     "rfknee");    //17

            makeJoint("hlshoulder", Vector3(-0.2, 0.5, 0.5),     "hshoulders");//18
            makeJoint("lelbow",     Vector3(-0.4, 0.25, 0.575),  "hlshoulder");//19
            makeJoint("lhand",      Vector3(-0.6, 0.0, 0.65),    "lelbow");    //20

            makeJoint("hrshoulder", Vector3(0.2, 0.5, 0.5),      "hshoulders");//21
            makeJoint("relbow",     Vector3(0.4, 0.25, 0.575),   "hrshoulder");//22
            makeJoint("rhand",      Vector3(0.6, 0.0, 0.65),     "relbow");    //23

            makeJoint("tail",       Vector3(0., 0., -0.7),       "hips");      //24

            // Symmetry
            makeSymmetric("lthigh", "rthigh");
            makeSymmetric("lhknee", "rhknee");
            makeSymmetric("lhheel", "rhheel");
            makeSymmetric("lhfoot", "rhfoot");

            makeSymmetric("lshoulder", "rshoulder");
            makeSymmetric("lfknee", "rfknee");
            makeSymmetric("lffoot", "rffoot");

            makeSymmetric("hlshoulder", "hrshoulder");
            makeSymmetric("lelbow", "relbow");
            makeSymmetric("lhand", "rhand");

            initCompressed();

            setFoot("lhfoot");
            setFoot("rhfoot");
            setFoot("lffoot");
            setFoot("rffoot");

            setFat("hips");
            setFat("shoulders");
            setFat("hshoulders");
            setFat("head");
        }
    };

    struct fromCsvFile : public ::Pinocchio::Skeleton {
        fromCsvFile(const std::string &filename) {

            std::ifstream csv_file("test.csv");
            std::vector<std::vector<std::string>> csv_data = Skeletons::readCSV(csv_file);

            std::vector<std::pair<std::string,std::string>> symmetries;
            std::vector<std::string> foot_bones;
            std::vector<std::string> fat_bones;

            int row_number = 0;
            std::vector<std::string> csv_header;
            for(auto const & row_data: csv_data) {
                if (!row_number) {
                    csv_header = row_data;
                    for (std::vector<std::string>::size_type i = 0; i != row_data.size(); i++) {
                        std::string & field_name = csv_header[i];
                        transform(field_name.begin(), field_name.end(), field_name.begin(), ::toupper); 
                    }
                } else {
                    std::string bone_name, parent_bone, symmetric_bone;
                    float x_coord, y_coord, z_coord;
                    bool is_foot, is_fat;

                    for (std::vector<std::string>::size_type i = 0; i != row_data.size(); i++) {
                        if (std::string("BONE") == csv_header[i])
                            bone_name = trim(row_data[i]);
                        if (std::string("X") == csv_header[i])
                            x_coord = std::stof(trim(row_data[i]));
                        if (std::string("Y") == csv_header[i])
                            y_coord = std::stof(trim(row_data[i]));
                        if (std::string("Z") == csv_header[i])
                            z_coord = std::stof(trim(row_data[i]));
                        if (std::string("PARENT") == csv_header[i])
                            parent_bone = trim(row_data[i]);
                        if (std::string("SYMMETRIC") == csv_header[i])
                            symmetric_bone = trim(row_data[i]);
                        if (std::string("FOOT") == csv_header[i])
                            is_foot = (trim(row_data[i]).length() != 0);
                        if (std::string("FAT") == csv_header[i])
                            is_fat = (trim(row_data[i]).length() != 0);
                    }
                    if (bone_name.length() > 0 && symmetric_bone.length() > 0) {
                        symmetries.push_back(make_pair(bone_name, symmetric_bone));
                    }
                    if (is_foot) {
                        foot_bones.push_back(bone_name);
                    }
                    if (is_fat) {
                        fat_bones.push_back(bone_name);
                    }

                    std::cout << "Bone: " << bone_name << " = " << x_coord << ", " << y_coord << ", " << z_coord << "; Parent = " << parent_bone << std::endl;
                    makeJoint(bone_name,  Vector3(x_coord, y_coord, z_coord), parent_bone);

                }
                row_number++;
            }

            for (auto const & symmetry: symmetries) {
                std::cout << "Symmetry: " << symmetry.first << " <-> " << symmetry.second << std::endl;
                makeSymmetric(symmetry.first, symmetry.second);
            }

            initCompressed();

            for (auto const & bone: foot_bones) {
                std::cout << "Foot Bone: " << bone << std::endl;
                setFoot(bone);
            }

            for (auto const & bone: fat_bones) {
                std::cout << "Fat Bone: " << bone << std::endl;
                setFat(bone);
            }

        }
    };


    struct fromFile : public ::Pinocchio::Skeleton {
        fromFile(const std::string &filename) {
            std::ifstream strm(filename.c_str());

            if (!strm.is_open()) {
                Debugging::out() << "Error opening file " << filename << std::endl;
                return;
            }

            while (!strm.eof()) {
                std::vector<std::string> line = readWords(strm);
                if (line.size() < 5) {                          // Error
                    continue;
                }

                Vector3 p;
                sscanf(line[1].c_str(), "%lf", &(p[0]));
                sscanf(line[2].c_str(), "%lf", &(p[1]));
                sscanf(line[3].c_str(), "%lf", &(p[2]));

                if (line[4] == "-1") {
                    line[4] = std::string();
                }

                makeJoint(line[0], p * 2., line[4]);
            }

            initCompressed();
        }
    };

} // namespace Skeletons


struct ArgData {
    ArgData() :
    stopAtMesh(false), stopAfterCircles(false), skelScale(1.), noFit(true),
        skeleton(Skeletons::Human()), stiffness(1.),
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
                out.skeleton = Skeletons::Human();
            } else if(curStr == std::string("horse")) {
                out.skeleton = Skeletons::Horse();
            } else if(curStr == std::string("quad")) {
                out.skeleton = Skeletons::Quad();
            } else if(curStr == std::string("centaur")) {
                out.skeleton = Skeletons::Centaur();
            } else {
                out.skeleton = Skeletons::fromFile(curStr);
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


int process(const std::vector<std::string> &args) {
    int i;
    ArgData a = processArgs(args);

    Debugging::setOutStream(std::cout);

    Mesh m(a.filename);

    if (m.vertices.size() == 0) {
        std::cout << "Error reading file.  Aborting." << std::endl;
        exit(0);
        return EXIT_FAILURE;
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
        for(i = 0; i < (int)o.embedding.size(); ++i)
            o.embedding[i] = m.toAdd + o.embedding[i] * m.scale;

        o.attachment = new Attachment(m, a.skeleton, o.embedding, tester, a.stiffness);

        delete tester;
        delete distanceField;
    }

    if (o.embedding.size() == 0) {
        std::cout << "Error embedding" << std::endl;
        return EXIT_FAILURE;
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

    return EXIT_SUCCESS;
}


int main (int argc, const char * const * argv, const char * const * envp) {
    auto skel = Skeletons::fromCsvFile("test.csv");

    std::vector<std::string> args;
    for(int i = 0; i < argc; ++i) {
        args.push_back(argv[i]);
    }
    return process(args);
}
