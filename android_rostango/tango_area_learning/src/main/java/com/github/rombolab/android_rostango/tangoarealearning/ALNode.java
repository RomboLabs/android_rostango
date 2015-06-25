package com.github.rombolab.android_rostango.tangoarealearning;

import android.content.Context;
import android.util.Log;

import com.google.atap.tangoservice.TangoPoseData;

import org.ros.namespace.GraphName;
import org.ros.node.ConnectedNode;
import org.ros.node.Node;
import org.ros.node.NodeMain;

import java.text.DecimalFormat;
import tango_msgs.TangoPoseDataMsg;

/**
 * Created by vijeth on 3/31/15.
 */
public class ALNode implements NodeMain {

    private static String TAG = ALNode.class.getSimpleName();
    private TangoPosePublisher mTangoPosePublisher;


    public boolean isStarted =false;

    public ALNode(Context context) {
        Log.i(TAG, "Build.MODEL=" + android.os.Build.MODEL);

        if (android.os.Build.MODEL.equals("Project Tango Tablet Development Kit")) {
            Log.i(TAG, "YELLOWSTONE device");
        } else if (android.os.Build.MODEL.equals("Peanut")) {
            Log.i(TAG, "PEANUT device");
        }
    }

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of("tango_area_learning");
    }

    @Override
    public void onStart(ConnectedNode node) {
        double test = 34;
        Log.i(TAG, "Starting Node");
        mTangoPosePublisher = new TangoPosePublisher(node);

        isStarted = true;
    }




    protected void onPause() {
    //    super.onPause();

    }


    protected void onResume() {
    //   super.onResume();

    }

    @Override
    public void onShutdown(Node node) {

        if (isStarted) {
            isStarted=false;
        }
    }

    @Override
    public void onShutdownComplete(Node node) {
    }

    @Override
    public void onError(Node node, Throwable throwable) {
    }



    public void publishPose(TangoPoseData pose_Tango){

        DecimalFormat threeDec = new DecimalFormat("0.000");
        String translationString = "[" + threeDec.format(pose_Tango.translation[0])
                + ", " + threeDec.format(pose_Tango.translation[1]) + ", "
                + threeDec.format(pose_Tango.translation[2]) + "] ";

        Log.i(TAG, "Pose to be messaged " + translationString);


        mTangoPosePublisher.setPoseMsg(pose_Tango);
        if(mTangoPosePublisher!=null) {
            mTangoPosePublisher.publishPose();
        }
    }



}
