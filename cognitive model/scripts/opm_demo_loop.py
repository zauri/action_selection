#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime

# ROS Imports
import rospy

# DAGAP Imports
from dagap_msgs.srv import *
from dagap_msgs.msg import *
import dagap.utils.tfwrapper as dagap_tf

# PyCRAM Imports
from pycram.process_module import simulated_robot
from pycram.designators.location_designator import *
from pycram.designators.action_designator import *
from pycram.enums import Arms
from pycram.designators.object_designator import *
from pycram.ros.tf_broadcaster import TFBroadcaster
from pycram.designator import ObjectDesignatorDescription
from pycram.pose import Pose
from pycram.plan_failures import IKError
from pycram.local_transformer import LocalTransformer


def opm_dagap_client(reference_frame: str, object_list: [OPMObjectQuery]) -> GetNextOPMObjectResponse:
    rospy.wait_for_service('dagap_opm_query')
    try:
        call_common_service = rospy.ServiceProxy('dagap_opm_query', GetNextOPMObject)
        srv = GetNextOPMObjectRequest(reference_frame, object_list)
        response = call_common_service(srv)
        return response
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)


def dagap_client(task_description: str, object_frame: [str]) -> GetGraspPoseResponse:
    rospy.wait_for_service('dagap_query')
    try:
        call_dagap_service = rospy.ServiceProxy('dagap_query', GetGraspPose)
        srv = GetGraspPoseRequest(task_description, object_frame)
        response = call_dagap_service(srv)
        return response
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)


class PickAndPlaceDemo:

    def __init__(self):
        self.reference_frame = "iai_kitchen/sink_area_surface"
        dagap_tf.init()  # call tfwrapper init()

        # Set up the bullet world
        self.world = BulletWorld()
        self.world.set_gravity([0, 0, -9.8])

        self.tfbroadcaster = TFBroadcaster()
        self.local_transformer = LocalTransformer()  # PyCRAM tf transformer

        # Spawn ground plane
        self.plane = Object(name="floor", type="environment", path="plane.urdf", world=self.world)
        # plane.set_color([0, 0, 0, 1])

        # Spawn kitchen
        self.kitchen = Object(name="kitchen", type="environment", path="kitchen.urdf")
        # kitchen.set_color([0.2, 0, 0.4, 0.6])
        self.kitchen_desig = ObjectDesignatorDescription(names=["kitchen"])

        sink_area_surface_frame = self.kitchen.get_link_tf_frame("sink_area_surface")
        kitchen_island_surface_frame = self.kitchen.get_link_tf_frame("kitchen_island_surface")

        self.object_spawning_poses: List[Pose] = [
            Pose([0.2, -0.15, 0.1], [0, 0, 1, 0], frame=sink_area_surface_frame),  # breakfast-cereal
            Pose([0.2, -0.35, 0.05], [0, 0, 1, 0], frame=sink_area_surface_frame),  # cup
            Pose([0.0, 0.5, 0.05], [0, 0, 0, 1], frame=kitchen_island_surface_frame),  # bowl
            Pose([0.15, -0.4, 0.1], [0, 0, 1, 0], frame=sink_area_surface_frame),  # spoon
            Pose([0.07, -0.35, 0.1], [0, 0, 1, 0], frame=sink_area_surface_frame)  # milk
        ]

        self.object_placing_poses: List[Pose] = [
            Pose([-0.2, -0.50, 0.1], [0, 0, 0, 1], frame=kitchen_island_surface_frame),  # breakfast-cereal
            Pose([-0.10, -0.80, 0.05], [0, 0, 0, 1], frame=kitchen_island_surface_frame),  # cup
            Pose([-0.24, -0.70, 0.05], [0.0, 0.0, 0.63, 0.77], frame=kitchen_island_surface_frame),  # bowl
            Pose([-0.24, -0.6, 0.1], [0, 0, 0, 1], frame=kitchen_island_surface_frame),  # spoon
            Pose([0.0, -1.00, 0.1], [0, 0, 1, 0], frame=kitchen_island_surface_frame)  # milk
        ]

        # Original poses
        # self.object_spawning_poses_sink: List[Pose] = [
        #     dagap_tf.list_to_pose([0.2, -0.15, 0.1], [0, 0, 0, 1]),  # breakfast-cereal
        #     dagap_tf.list_to_pose([0.2, -0.35, 0.05], [0, 0, 0, 1]),  # cup
        #     dagap_tf.list_to_pose([0.20, -0.75, 0.05], [0, 0, 0, 1]),  # bowl
        #     dagap_tf.list_to_pose([0.15, -0.4, 0.1], [0, 0, 0, 1]),  # spoon
        #     dagap_tf.list_to_pose([0.07, -0.35, 0.1], [0, 0, 0, 1])  # milk
        # ]

        # transform_sink_map = lookup_transform(frame, u'map')

        # Hint for type of list object_spawning_poses_map
        self.object_spawning_poses_map: List[Pose] = []
        self.object_placing_poses_map: List[Pose] = []

        # Transform poses to map frame for correct spawn pose
        element: Pose  # Hint for type of element
        for element in self.object_spawning_poses:
            self.object_spawning_poses_map.append(
                # dagap_tf.transform_pose(element, 'simulated/map', element.header.frame_id))
                self.local_transformer.transform_pose(element, target_frame="map"))

        # Transform object_placing_poses into map frame
        element: Pose  # Hint for type of element
        for element in self.object_placing_poses:
            self.object_placing_poses_map.append((
                self.local_transformer.transform_pose(element, target_frame="map")
            ))

        self.object_names = [
            "robot",
            "breakfast-cereal",
            "cup",
            "bowl",
            "spoon",
            "milk"
        ]

        self.query_object_list_map: List[OPMObjectQuery] = [
            OPMObjectQuery(Object="robot", object_location=Pose([0, 0, 0])),  # OPM needs robot in first element
            OPMObjectQuery(Object="breakfast-cereal", object_location=self.object_spawning_poses_map[0]),
            OPMObjectQuery(Object="cup", object_location=self.object_spawning_poses_map[1]),
            OPMObjectQuery(Object="bowl", object_location=self.object_spawning_poses_map[2]),
            OPMObjectQuery(Object="spoon", object_location=self.object_spawning_poses_map[3]),
            OPMObjectQuery(Object="milk", object_location=self.object_spawning_poses_map[4])
        ]

        # Spawn breakfast cereal
        # TODO: change self.query_object_list_map to original pose list self.object_spawning_poses_map
        self.breakfast_cereal = Object(self.query_object_list_map[1].Object,
                                       self.query_object_list_map[1].Object,
                                       path="breakfast_cereal.stl",
                                       pose=self.query_object_list_map[1].object_location)
        self.breakfast_cereal_desig = ObjectDesignatorDescription(names=[self.query_object_list_map[1].Object])
        # Spawn cup
        self.cup = Object(self.query_object_list_map[2].Object,
                          self.query_object_list_map[2].Object,
                          path="../resources/cup.stl",
                          pose=self.query_object_list_map[2].object_location)
        self.cup_desig = ObjectDesignatorDescription(names=[self.query_object_list_map[2].Object])
        # Spawn bowl
        self.bowl = Object(self.query_object_list_map[3].Object,
                           self.query_object_list_map[3].Object,
                           path="bowl.stl",
                           pose=self.query_object_list_map[3].object_location)
        self.bowl_desig = ObjectDesignatorDescription(names=[self.query_object_list_map[3].Object])
        # Spawn spoon
        self.spoon = Object(self.query_object_list_map[4].Object,
                            self.query_object_list_map[4].Object,
                            path="spoon.stl",
                            pose=self.query_object_list_map[4].object_location)
        self.spoon_desig = ObjectDesignatorDescription(names=[self.query_object_list_map[4].Object])
        # Spawn milk
        self.milk = Object(self.query_object_list_map[5].Object,
                           self.query_object_list_map[5].Object,
                           path="milk.stl",
                           pose=self.query_object_list_map[5].object_location)
        self.milk_desig = ObjectDesignatorDescription(names=[self.query_object_list_map[5].Object])

        # Spawn PR2 robot
        self.pr2 = Object(name="pr2", type="robot", path="pr2.urdf", pose=Pose([0, 0, 0]))
        self.robot_desig = ObjectDesignatorDescription(names=["pr2"]).resolve()

        self.query_object_list_map[1].object_frame =\
            ("simulated/" + self.breakfast_cereal.get_link_tf_frame(link_name="").replace("/", ""))
        self.query_object_list_map[2].object_frame =\
            ("simulated/" + self.cup.get_link_tf_frame(link_name="").replace("/", ""))
        self.query_object_list_map[3].object_frame =\
            ("simulated/" + self.bowl.get_link_tf_frame(link_name="").replace("/", ""))
        self.query_object_list_map[4].object_frame =\
            ("simulated/" + self.spoon.get_link_tf_frame(link_name="").replace("/", ""))
        self.query_object_list_map[5].object_frame =\
            ("simulated/" + self.milk.get_link_tf_frame(link_name="").replace("/", ""))

        self.world.add_vis_axis(self.bowl.get_pose())
        self.world.add_vis_axis(self.breakfast_cereal.get_pose())
        self.world.add_vis_axis(self.cup.get_pose())
        self.world.add_vis_axis(self.spoon.get_pose())
        self.world.add_vis_axis(self.milk.get_pose())

        # Test out an example transform to catch exceptions early
        if dagap_tf.lookup_transform("simulated/" + self.kitchen.get_link_tf_frame("sink_area_surface"),
                                     "simulated/" + self.bowl.tf_frame):
            rospy.loginfo("Test succeeded: Found transform")
        else:
            rospy.logwarn("Test failed: Did not find transform")

    def get_designator_from_name(self, object_name: str) -> ObjectDesignatorDescription:
        if self.object_names[0] == object_name:
            return self.robot_desig
        if self.object_names[1] == object_name:
            return self.breakfast_cereal_desig
        if self.object_names[2] == object_name:
            return self.cup_desig
        if self.object_names[3] == object_name:
            return self.bowl_desig
        if self.object_names[4] == object_name:
            return self.spoon_desig
        if self.object_names[5] == object_name:
            return self.milk_desig

    def get_object_from_name(self, object_name: str) -> Object:
        if self.object_names[0] == object_name:
            return self.pr2
        if self.object_names[1] == object_name:
            return self.breakfast_cereal
        if self.object_names[2] == object_name:
            return self.cup
        if self.object_names[3] == object_name:
            return self.bowl
        if self.object_names[4] == object_name:
            return self.spoon
        if self.object_names[5] == object_name:
            return self.milk

    def get_name_from_frame(self, frame: str) -> str:
        for name in self.object_names:
            if name in frame:
                return name
        rospy.logwarn("[get_name_from_frame]: Could not find name.")
        return ""

    def get_placing_pose_from_name(self, object_name: str) -> Pose:
        if self.object_names[1] == object_name:
            return self.object_placing_poses_map[0]
        if self.object_names[2] == object_name:
            return self.object_placing_poses_map[1]
        if self.object_names[3] == object_name:
            return self.object_placing_poses_map[2]
        if self.object_names[4] == object_name:
            return self.object_placing_poses_map[3]
        if self.object_names[5] == object_name:
            return self.object_placing_poses_map[4]

    def run(self, cool_demo: bool = True):
        """

        Parameters
        ----------
        cool_demo: Variable to determine if demo uses OPM/DAGAP service or runs conservatively
        """
        start_time = rospy.get_time()

        rospy.loginfo("Running demo.")
        rospy.loginfo("Start time: %i", start_time)
        with (simulated_robot):
            # Send request to DAGAP service
            rospy.set_param(param_name='robot_root',
                            param_value="simulated/" + self.pr2.get_link_tf_frame(link_name=""))

            object_list = self.query_object_list_map

            while len(object_list) > 1:

                if cool_demo:
                    # service return frame not the name
                    res: GetNextOPMObjectResponse = opm_dagap_client(reference_frame=self.reference_frame,
                                                                     object_list=object_list)
                    rospy.loginfo("Received answer:")
                    print(res)
                else:
                    # if conservative demo take next object in list
                    res = GetNextOPMObjectResponse(next_object=object_list[1].object_frame,
                                                   hand='left')
                    pass

                ParkArmsAction([Arms.BOTH]).resolve().perform()
                MoveTorsoAction([0.33]).resolve().perform()

                next_object_name = self.get_name_from_frame(res.next_object)
                next_object_desig: ObjectDesignatorDescription = self.get_designator_from_name(next_object_name)

                # Remove current object from list for next iteration
                for element in list(object_list):
                    if element.Object == next_object_name:
                        object_list.remove(element)

                pickup_pose = CostmapLocation(target=next_object_desig.resolve(),
                                              reachable_for=self.robot_desig
                                              ).resolve()
                # pickup_arm = pickup_pose.reachable_arms[0]  # allocate an arm to the grasping task

                NavigateAction(target_locations=[pickup_pose.pose]).resolve().perform()

                # if cool_demo:
                #     description = "Pick up"
                #     gripper: GetGraspPoseResponse = dagap_client(task_description=description,
                #                                                  object_frame=[res.next_object])

                #     if "l_gripper" in gripper.grasp_pose[0].header.frame_id:
                #         pickup_arm = "left"
                #         rospy.loginfo("Picking up object with {} hand.".format(pickup_arm))
                #     elif "r_gripper" in gripper.grasp_pose[0].header.frame_id:
                #         pickup_arm = "right"
                #         rospy.loginfo("Picking up object with {} hand.".format(pickup_arm))
                #     else:
                #         rospy.logwarn("Could not allocate a gripper.")
                # else:  # if conservative demo
                pickup_arm = pickup_pose.reachable_arms[0]

                try:
                    rospy.loginfo("Picking up {}".format(next_object_name))
                    PickUpAction(object_designator_description=next_object_desig,
                                 arms=[pickup_arm],
                                 grasps=["front"]
                                 ).resolve().perform()
                except IKError:
                    rospy.logwarn("Failed execution with {} hand.".format(pickup_arm))
                    if pickup_arm == "left":
                        pickup_arm = "right"
                        rospy.loginfo("Falling back to {} hand.".format(pickup_arm))
                    elif pickup_arm == "right":
                        pickup_arm = "left"
                        rospy.loginfo("Falling back to {} hand.".format(pickup_arm))
                    PickUpAction(object_designator_description=next_object_desig, arms=[pickup_arm],
                                 grasps=["front"]
                                 ).resolve().perform()

                ParkArmsAction([Arms.BOTH]).resolve().perform()
                # Get placing position on island
                # place_island = SemanticCostmapLocation(urdf_link_name="kitchen_island_surface",
                #                                        part_of=self.kitchen_desig.resolve(),
                #                                        for_object=next_object_desig.resolve()
                #                                        ).resolve()

                # self.world.remove_vis_axis()

                # Visualize coordinate system of kitchen island
                nullpose = dagap_tf.transform_pose(
                    pose=Pose(),
                    target_frame="simulated/map",
                    source_frame="simulated/" + self.kitchen.get_link_tf_frame("kitchen_island_surface")
                ).pose
                self.world.add_vis_axis(
                    Pose(dagap_tf.point_to_list(nullpose.position), dagap_tf.quaternion_to_list(nullpose.orientation)))

                next_placing_pose = self.get_placing_pose_from_name(next_object_name)
                self.world.add_vis_axis(next_placing_pose)

                # Get position to stand while placing the object
                place_stand = CostmapLocation(target=next_placing_pose,
                                              reachable_for=self.robot_desig,
                                              reachable_arm=pickup_arm
                                              ).resolve()

                NavigateAction(target_locations=[place_stand.pose]).resolve().perform()

                rospy.loginfo("Placing {} on kitchen island.".format(next_object_name))
                PlaceAction(object_designator_description=next_object_desig,
                            target_locations=[next_placing_pose],
                            arms=[pickup_arm]
                            ).resolve().perform()
                ParkArmsAction([Arms.BOTH]).resolve().perform()

                end_time = rospy.get_time()

                rospy.loginfo("End of demo.")
                rospy.loginfo("End time: %i", end_time)

                self.world.remove_vis_axis()  # Remove visualizations
        #self.world.exit()


if __name__ == "__main__":
    print("Starting demo")

    # cool_demo=True, use OPM/DAGAP services
    # cool_demo=False, follow list order when placing the objects (conservative demo with predefined sequence)
    for i in range(0,10):
        Demo = PickAndPlaceDemo()  # init demo and spawn objects
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Start demo {}: {}".format(i, current_time))
        Demo.run(cool_demo=True)  # run demo
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("End demo {}: {}".format(i, current_time))
