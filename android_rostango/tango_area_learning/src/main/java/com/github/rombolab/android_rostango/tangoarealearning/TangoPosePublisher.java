package com.github.rombolab.android_rostango.tangoarealearning;
import android.util.Log;

import com.google.atap.tangoservice.TangoCoordinateFramePair;
import com.google.atap.tangoservice.TangoPoseData;

import org.ros.message.Time;
import org.ros.node.ConnectedNode;
import org.ros.node.topic.Publisher;

import java.text.DecimalFormat;

import tango_msgs.TangoCoordinateFramePairMsg;
import tango_msgs.TangoCoordinateFrameTypeMsg;
import tango_msgs.TangoPoseDataMsg;
import tango_msgs.TangoPoseStatusTypeMsg;

/**
 * Created by vijeth on 6/13/15.
 */
public class TangoPosePublisher {
    private TangoPoseDataMsg pose_msg;
    private Publisher<TangoPoseDataMsg> publisher;
    private ConnectedNode pConnectedNode;
    private static String TAG = TangoPosePublisher.class.getSimpleName();

    public TangoPosePublisher(ConnectedNode connectedNode){
        pConnectedNode = connectedNode;
        pose_msg = connectedNode.getTopicMessageFactory().newFromType(TangoPoseDataMsg._TYPE);
        publisher = connectedNode.newPublisher("/tango_pose", TangoPoseDataMsg._TYPE);
    }

    public void setPoseMsg(TangoPoseData pose_Tango){
     //  pose_msg.getVersion().setVersion(pose_Tango.version);
        pose_msg.setTimestamp(pose_Tango.timestamp);


      // int targetFrame=pose_Tango.targetFrame;
       setFrames(pose_Tango.baseFrame,pose_Tango.targetFrame) ;

       setStatus(pose_Tango.statusCode) ;
       double translation[]= pose_Tango.translation;
       setTranslation(translation);

       double orientation[] = pose_Tango.rotation;
       setOrientation(orientation) ;


    }

    public void setStatus(int statusCode)
    {
       // TangoPoseStatusTypeMsg statusCodeMsg = pConnectedNode.getTopicMessageFactory().newFromType(TangoPoseStatusTypeMsg._TYPE) ;
        TangoPoseStatusTypeMsg statusCodeMsg=pose_msg.getStatusCode();

        switch (statusCode) {
            case TangoPoseData.POSE_INITIALIZING:
                statusCodeMsg.setStatus(TangoPoseStatusTypeMsg.TANGO_POSE_INITIALIZING);
                Log.i(TAG, "Status Initializing " + statusCode);
                break;

            case TangoPoseData.POSE_INVALID:
                statusCodeMsg.setStatus(TangoPoseStatusTypeMsg.TANGO_POSE_INVALID);
                Log.i(TAG, "Status InValid " + statusCode);
                break;

            case TangoPoseData.POSE_VALID:
                statusCodeMsg.setStatus(TangoPoseStatusTypeMsg.TANGO_POSE_VALID);
             //   statusCodeMsg.equals(TangoPoseStatusTypeMsg.TANGO_POSE_VALID);
                Log.i(TAG, "Status Valid " + statusCode);
                break;

            default:
                statusCodeMsg.setStatus(TangoPoseStatusTypeMsg.TANGO_POSE_UNKNOWN);
                Log.i(TAG, "Status Unknown " + statusCode);
                break;
        }

        pose_msg.setStatusCode(statusCodeMsg);
    }



    public void setFrames(int baseFrame,int targetFrame) {
        TangoCoordinateFramePairMsg framePairMsg = pConnectedNode.getTopicMessageFactory().newFromType(TangoCoordinateFramePairMsg._TYPE);


        if (baseFrame == TangoPoseData.COORDINATE_FRAME_AREA_DESCRIPTION
                && targetFrame == TangoPoseData.COORDINATE_FRAME_DEVICE) {
            framePairMsg.setBase(TangoCoordinateFrameTypeMsg.TANGO_COORDINATE_FRAME_AREA_DESCRIPTION);
            framePairMsg.setTarget(TangoCoordinateFrameTypeMsg.TANGO_COORDINATE_FRAME_DEVICE);
        }

        if (baseFrame == TangoPoseData.COORDINATE_FRAME_START_OF_SERVICE
                && targetFrame == TangoPoseData.COORDINATE_FRAME_DEVICE) {
            framePairMsg.setBase(TangoCoordinateFrameTypeMsg.TANGO_COORDINATE_FRAME_START_OF_SERVICE);
            framePairMsg.setTarget(TangoCoordinateFrameTypeMsg.TANGO_COORDINATE_FRAME_DEVICE);

        }

        if (baseFrame == TangoPoseData.COORDINATE_FRAME_AREA_DESCRIPTION
                && targetFrame == TangoPoseData.COORDINATE_FRAME_START_OF_SERVICE) {
            framePairMsg.setBase(TangoCoordinateFrameTypeMsg.TANGO_COORDINATE_FRAME_AREA_DESCRIPTION);
            framePairMsg.setTarget(TangoCoordinateFrameTypeMsg.TANGO_COORDINATE_FRAME_START_OF_SERVICE);
        }

        pose_msg.setFrame(framePairMsg);
    }

    public void setTranslation(double translation[])
    {
    pose_msg.setTranslation(translation);
    }

    public  void setOrientation(double orientation[])
    {
        pose_msg.setOrientation(orientation);
    }

    public void publishPose() {

        DecimalFormat threeDec = new DecimalFormat("0.000");
        double msg_translation[]= pose_msg.getTranslation();
        String translationString = "[" + threeDec.format(msg_translation[0])
                + ", " + threeDec.format(msg_translation[1]) + ", "
                + threeDec.format(msg_translation[2]) + "] ";

        Log.i(TAG, "Pose to be messaged " + translationString);
        publisher.publish(pose_msg);

    }

/*
    public void publishPose(){
        long lt = System.currentTimeMillis();
        Time t = new Time((int) (lt / 1e3), (int) ((lt % 1e3) * 1e6));
        pose.getHeader().setStamp(t);
        pose.getHeader().setFrameId("/global");
        publisher.publish(pose);
    }
    */
}
