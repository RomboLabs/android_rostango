package com.github.rombolab.android_rostango.tangoarealearning;

import android.app.FragmentManager;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.atap.tangoservice.Tango;
import com.google.atap.tangoservice.Tango.OnTangoUpdateListener;
import com.google.atap.tangoservice.TangoAreaDescriptionMetaData;
import com.google.atap.tangoservice.TangoConfig;
import com.google.atap.tangoservice.TangoCoordinateFramePair;
import com.google.atap.tangoservice.TangoErrorException;
import com.google.atap.tangoservice.TangoEvent;
import com.google.atap.tangoservice.TangoInvalidException;
import com.google.atap.tangoservice.TangoOutOfDateException;
import com.google.atap.tangoservice.TangoPoseData;
import com.google.atap.tangoservice.TangoXyzIjData;
import  com.github.rombolab.android_rostango.tangoarealearning.SetADFNameDialog.SetNameCommunicator;

import org.ros.android.RosActivity;
import org.ros.node.NodeConfiguration;
import org.ros.node.NodeMainExecutor;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class AreaLearningActivity extends RosActivity implements View.OnClickListener, SetNameCommunicator  {
    private static String TAG = AreaLearningActivity.class.getSimpleName();

    private ALNode mALNode ;


    // Tango variable declarations
    private static final int SECONDS_TO_MILLI = 1000;
    private Tango mTango;
    private TangoConfig mConfig;


    // View Declarations
    private TextView mTangoEventTextView;
    private TextView mTangoServiceVersionTextView;
    private TextView mApplicationVersionTextView;
    private TextView mUUIDTextView;


    private TextView mStart2DeviceTranslationTextView;
    private TextView mStart2DeviceQuatTextView;
    private TextView mStart2DevicePoseStatusTextView;
    private TextView mStart2DevicePoseCountTextView;
    private TextView mStart2DevicePoseDeltaTextView;

    private TextView mAdf2DeviceTranslationTextView;
    private TextView mAdf2DeviceQuatTextView;
    private TextView mAdf2DevicePoseStatusTextView;
    private TextView mAdf2DevicePoseCountTextView;
    private TextView mAdf2DevicePoseDeltaTextView;

    private TextView mAdf2StartTranslationTextView;
    private TextView mAdf2StartQuatTextView;
    private TextView mAdf2StartPoseStatusTextView;
    private TextView mAdf2StartPoseCountTextView;
    private TextView mAdf2StartPoseDeltaTextView;

    //Buttons

    private Button mSaveAdf;
    private Button mFirstPersonButton;
    private Button mThirdPersonButton;
    private Button mTopDownButton;

    private int mStart2DevicePoseCount;
    private int mStart2DevicePreviousPoseStatus;
    private double mStart2DevicePoseDelta;
    private double mStart2DevicePreviousPoseTimeStamp;

    private int mAdf2DevicePoseCount;
    private int mAdf2DevicePreviousPoseStatus;
    private double mAdf2DevicePoseDelta;
    private double mAdf2DevicePreviousPoseTimeStamp;

    private int mAdf2StartPoseCount;
    private int mAdf2StartPreviousPoseStatus;
    private double mAdf2StartPoseDelta;
    private double mAdf2StartPreviousPoseTimeStamp;


    private boolean mIsRelocalized;
    private boolean mIsLearningMode;
    private boolean mIsConstantSpaceRelocalize;

    private String mCurrentUUID;

//
//    private ALRenderer mRenderer;
//    private GLSurfaceView mGLView;

    public AreaLearningActivity() {
        super("Area Learning App", "Area Learning App");
    }

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_area_learning);

        mTangoEventTextView = (TextView) findViewById(R.id.tangoevent);

        mAdf2DeviceTranslationTextView = (TextView) findViewById(R.id.adf2devicePose);
        mStart2DeviceTranslationTextView = (TextView) findViewById(R.id.start2devicePose);
        mAdf2StartTranslationTextView = (TextView) findViewById(R.id.adf2startPose);
        mAdf2DeviceQuatTextView = (TextView) findViewById(R.id.adf2deviceQuat);
        mStart2DeviceQuatTextView = (TextView) findViewById(R.id.start2deviceQuat);
        mAdf2StartQuatTextView = (TextView) findViewById(R.id.adf2startQuat);

        mAdf2DevicePoseStatusTextView = (TextView) findViewById(R.id.adf2deviceStatus);
        mStart2DevicePoseStatusTextView = (TextView) findViewById(R.id.start2deviceStatus);
        mAdf2StartPoseStatusTextView = (TextView) findViewById(R.id.adf2startStatus);

        mAdf2DevicePoseCountTextView = (TextView) findViewById(R.id.adf2devicePosecount);
        mStart2DevicePoseCountTextView = (TextView) findViewById(R.id.start2devicePosecount);
        mAdf2StartPoseCountTextView = (TextView) findViewById(R.id.adf2startPosecount);

        mAdf2DevicePoseDeltaTextView = (TextView) findViewById(R.id.adf2deviceDeltatime);
        mStart2DevicePoseDeltaTextView = (TextView) findViewById(R.id.start2deviceDeltatime);
        mAdf2StartPoseDeltaTextView = (TextView) findViewById(R.id.adf2startDeltatime);


        mTangoServiceVersionTextView = (TextView) findViewById(R.id.version);
        mApplicationVersionTextView = (TextView) findViewById(R.id.appversion);

        mFirstPersonButton = (Button) findViewById(R.id.first_person_button);
        mThirdPersonButton = (Button) findViewById(R.id.third_person_button);
        mTopDownButton = (Button) findViewById(R.id.top_down_button);

        mSaveAdf = (Button) findViewById(R.id.saveAdf);
        mUUIDTextView = (TextView) findViewById(R.id.uuid);

        mSaveAdf.setVisibility(View.GONE);

        // Set up button click listeners
        mFirstPersonButton.setOnClickListener(this);
        mThirdPersonButton.setOnClickListener(this);
        mTopDownButton.setOnClickListener(this);

/*        PackageInfo packageInfo;
        try {
            packageInfo = this.getPackageManager().getPackageInfo(this.getPackageName(), 0);
            mApplicationVersionTextView.setText(packageInfo.versionName);
        } catch (NameNotFoundException e) {
            e.printStackTrace();
        }*/


        // Instantiate the Tango service
        mTango = new Tango(this);
        mIsRelocalized = false;

        Intent intent = getIntent();
        mIsLearningMode = intent.getBooleanExtra(ALStartActivity.USE_AREA_LEARNING, false);
        mIsConstantSpaceRelocalize = intent.getBooleanExtra(ALStartActivity.LOAD_ADF, false);


        setTangoConfig();
    }


    @Override
    protected void init(NodeMainExecutor nodeMainExecutor) {

        mALNode = new ALNode(this);


        NodeConfiguration nodeConfiguration = NodeConfiguration.newPublic(getRosHostname());
        // At this point, the user has already been prompted to either enter the URI
        // of a master to use or to start a master locally.
        nodeConfiguration.setMasterUri(getMasterUri());
        Log.i(TAG, "Config Done");
        nodeMainExecutor.execute(mALNode, nodeConfiguration);


    }


    private void setTangoConfig() {
        mConfig = mTango.getConfig(TangoConfig.CONFIG_TYPE_CURRENT);

        // Check if learning mode
        if (mIsLearningMode) {
            // Set learning mode to config.
            mConfig.putBoolean(TangoConfig.KEY_BOOLEAN_LEARNINGMODE, true);
            // Set the ADF save button visible.
            mSaveAdf.setVisibility(View.VISIBLE);
            mSaveAdf.setOnClickListener(this);
        }
        // Check for Load ADF/Constant Space relocalization mode
        if (mIsConstantSpaceRelocalize) {
            ArrayList<String> fullUUIDList = new ArrayList<String>();
            // Returns a list of ADFs with their UUIDs
            fullUUIDList = mTango.listAreaDescriptions();
            if (fullUUIDList.size() == 0) {
                mUUIDTextView.setText(R.string.no_uuid);
            }

            // Load the latest ADF if ADFs are found.
            if (fullUUIDList.size() > 0) {
                mConfig.putString(TangoConfig.KEY_STRING_AREADESCRIPTION,
                        fullUUIDList.get(fullUUIDList.size() - 1));
                mUUIDTextView.setText(getString(R.string.number_of_adfs) + fullUUIDList.size()
                        + getString(R.string.latest_adf_is)
                        + fullUUIDList.get(fullUUIDList.size() - 1));
            }
        }

        // Set the number of loop closures to zero at start.
        mStart2DevicePoseCount = 0;
        mAdf2DevicePoseCount = 0;
        mAdf2StartPoseCount = 0;
        mTangoServiceVersionTextView.setText(mConfig.getString("tango_service_library_version"));
    }


    @Override
    protected void onPause() {
        super.onPause();
        try {
            mTango.disconnect();
        } catch (TangoErrorException e) {
            Toast.makeText(getApplicationContext(), R.string.tango_error, Toast.LENGTH_SHORT)
                    .show();
        }

        if (mALNode != null) {
            mALNode.onPause();
        }
    }


    @Override
    protected void onResume() {

        super.onResume();
        try {
            setUpTangoListeners();
        } catch (TangoErrorException e) {
            Toast.makeText(getApplicationContext(), R.string.tango_error, Toast.LENGTH_SHORT)
                    .show();
        } catch (SecurityException e) {
            Toast.makeText(getApplicationContext(), R.string.no_permissions, Toast.LENGTH_SHORT)
                    .show();
        }
        try {
            mTango.connect(mConfig);
        } catch (TangoOutOfDateException e) {
            Toast.makeText(getApplicationContext(), R.string.tango_out_of_date_exception,
                    Toast.LENGTH_SHORT).show();
        } catch (TangoErrorException e) {
            Toast.makeText(getApplicationContext(), R.string.tango_error, Toast.LENGTH_SHORT)
                    .show();
        }
        if (mALNode != null) {
            mALNode.onResume();
        }

    }


    private void setUpTangoListeners() {

        // Set Tango Listeners for Poses Device wrt Start of Service, Device wrt
        // ADF and Start of Service wrt ADF
        ArrayList<TangoCoordinateFramePair> framePairs = new ArrayList<TangoCoordinateFramePair>();
        framePairs.add(new TangoCoordinateFramePair(
                TangoPoseData.COORDINATE_FRAME_START_OF_SERVICE,
                TangoPoseData.COORDINATE_FRAME_DEVICE));
        framePairs.add(new TangoCoordinateFramePair(
                TangoPoseData.COORDINATE_FRAME_AREA_DESCRIPTION,
                TangoPoseData.COORDINATE_FRAME_DEVICE));
        framePairs.add(new TangoCoordinateFramePair(
                TangoPoseData.COORDINATE_FRAME_AREA_DESCRIPTION,
                TangoPoseData.COORDINATE_FRAME_START_OF_SERVICE));

        mTango.connectListener(framePairs, new OnTangoUpdateListener() {
            @Override
            public void onXyzIjAvailable(TangoXyzIjData xyzij) {
                // Not using XyzIj data for this sample
            }

            // Listen to Tango Events
            @Override
            public void onTangoEvent(final TangoEvent event) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        mTangoEventTextView.setText(event.eventKey + ": " + event.eventValue);
                    }
                });
            }

            @Override
            public void onPoseAvailable(TangoPoseData pose) {

                // Update the text views with Pose info.
                updateTextViewWith(pose);
                if(mALNode.isStarted){
                    mALNode.publishPose(pose);
                }
 //               float[] translation = pose.getTranslationAsFloats();
 //               boolean updateRenderer = false;
 //               if (mIsRelocalized) {
 //                   if (pose.baseFrame == TangoPoseData.COORDINATE_FRAME_AREA_DESCRIPTION
 //                           && pose.targetFrame == TangoPoseData.COORDINATE_FRAME_DEVICE) {
 //                       updateRenderer = true;
 //                       mRenderer.getGreenTrajectory().updateTrajectory(translation);
 //                   }
 //               } else {
 //                   if (pose.baseFrame == TangoPoseData.COORDINATE_FRAME_START_OF_SERVICE
 //                           && pose.targetFrame == TangoPoseData.COORDINATE_FRAME_DEVICE) {
 //                       updateRenderer = true;
 //                       mRenderer.getBlueTrajectory().updateTrajectory(translation);
 //                   }
 //               }
 //
 //               // Update the trajectory, model matrix, and view matrix, then
 //               // render the scene again
 //               if (updateRenderer) {
 //                   mRenderer.getModelMatCalculator().updateModelMatrix(translation,
 //                           pose.getRotationAsFloats());
 //                   mRenderer.updateViewMatrix();
 //                   mGLView.requestRender();
 //               }
            }
        });
    }

    private void saveAdf() {
        showSetNameDialog();
    }

    private void showSetNameDialog() {
        Bundle bundle = new Bundle();
        if (mCurrentUUID != null) {
            try {
                TangoAreaDescriptionMetaData metaData = mTango
                        .loadAreaDescriptionMetaData(mCurrentUUID);
                byte[] adfNameBytes = metaData.get(TangoAreaDescriptionMetaData.KEY_NAME);
                if (adfNameBytes != null) {
                    String fillDialogName = new String(adfNameBytes);
                    bundle.putString(TangoAreaDescriptionMetaData.KEY_NAME, fillDialogName);
                }
            } catch (TangoErrorException e) {
            }
            bundle.putString(TangoAreaDescriptionMetaData.KEY_UUID, mCurrentUUID);
        }
        FragmentManager manager = getFragmentManager();
        SetADFNameDialog setADFNameDialog = new SetADFNameDialog();
        setADFNameDialog.setArguments(bundle);
        setADFNameDialog.show(manager, "ADFNameDialog");
    }

    @Override
    public void onSetName(String name, String uuids) {

        TangoAreaDescriptionMetaData metadata = new TangoAreaDescriptionMetaData();
        try {
            mCurrentUUID = mTango.saveAreaDescription();
            metadata = mTango.loadAreaDescriptionMetaData(mCurrentUUID);
            metadata.set(TangoAreaDescriptionMetaData.KEY_NAME, name.getBytes());
            mTango.saveAreaDescriptionMetadata(mCurrentUUID, metadata);
        } catch (TangoErrorException e) {
            Toast.makeText(getApplicationContext(), getString(R.string.tango_error),
                    Toast.LENGTH_SHORT).show();
            return;
        } catch (TangoInvalidException e) {
            Toast.makeText(getApplicationContext(), getString(R.string.tango_invalid),
                    Toast.LENGTH_SHORT).show();
            return;
        }
        Toast.makeText(getApplicationContext(), getString(R.string.adf_save) + mCurrentUUID,
                Toast.LENGTH_SHORT).show();
    }
    /**
     * Updates the text view in UI screen with the Pose. Each pose is associated with Target and
     * Base Frame. We need to check for that pair ad update our views accordingly.
     *
     * @param pose
     */
    private void updateTextViewWith(final TangoPoseData pose) {
        final DecimalFormat threeDec = new DecimalFormat("0.000");
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                String translationString = "[" + threeDec.format(pose.translation[0]) + ","
                        + threeDec.format(pose.translation[1]) + ","
                        + threeDec.format(pose.translation[2]) + "] ";

                String quaternionString = "[" + threeDec.format(pose.rotation[0]) + ","
                        + threeDec.format(pose.rotation[1]) + ","
                        + threeDec.format(pose.rotation[2]) + ","
                        + threeDec.format(pose.rotation[3]) + "] ";

                if (pose.baseFrame == TangoPoseData.COORDINATE_FRAME_AREA_DESCRIPTION
                        && pose.targetFrame == TangoPoseData.COORDINATE_FRAME_DEVICE) {
                    if (mAdf2DevicePreviousPoseStatus != pose.statusCode) {
                        mAdf2DevicePoseCount = 0;
                    }
                    mAdf2DevicePreviousPoseStatus = pose.statusCode;
                    mAdf2DevicePoseCount++;
                    mAdf2DevicePoseDelta = (pose.timestamp - mAdf2DevicePreviousPoseTimeStamp)
                            * SECONDS_TO_MILLI;
                    mAdf2DevicePreviousPoseTimeStamp = pose.timestamp;
                    mAdf2DeviceTranslationTextView.setText(translationString);
                    mAdf2DeviceQuatTextView.setText(quaternionString);
                    mAdf2DevicePoseStatusTextView.setText(getPoseStatus(pose));
                    mAdf2DevicePoseCountTextView.setText(Integer.toString(mAdf2DevicePoseCount));
                    mAdf2DevicePoseDeltaTextView.setText(threeDec.format(mAdf2DevicePoseDelta));
                }

                if (pose.baseFrame == TangoPoseData.COORDINATE_FRAME_START_OF_SERVICE
                        && pose.targetFrame == TangoPoseData.COORDINATE_FRAME_DEVICE) {
                    if (mStart2DevicePreviousPoseStatus != pose.statusCode) {
                        mStart2DevicePoseCount = 0;
                    }
                    mStart2DevicePreviousPoseStatus = pose.statusCode;
                    mStart2DevicePoseCount++;
                    mStart2DevicePoseDelta = (pose.timestamp - mStart2DevicePreviousPoseTimeStamp)
                            * SECONDS_TO_MILLI;
                    mStart2DevicePreviousPoseTimeStamp = pose.timestamp;
                    mStart2DeviceTranslationTextView.setText(translationString);
                    mStart2DeviceQuatTextView.setText(quaternionString);
                    mStart2DevicePoseStatusTextView.setText(getPoseStatus(pose));
                    mStart2DevicePoseCountTextView
                            .setText(Integer.toString(mStart2DevicePoseCount));
                    mStart2DevicePoseDeltaTextView.setText(threeDec.format(mStart2DevicePoseDelta));
                }

                if (pose.baseFrame == TangoPoseData.COORDINATE_FRAME_AREA_DESCRIPTION
                        && pose.targetFrame == TangoPoseData.COORDINATE_FRAME_START_OF_SERVICE) {
                    if (mAdf2StartPreviousPoseStatus != pose.statusCode) {
                        mAdf2StartPoseCount = 0;
                    }
                    mAdf2StartPreviousPoseStatus = pose.statusCode;
                    mAdf2StartPoseCount++;
                    mAdf2StartPoseDelta = (pose.timestamp - mAdf2StartPreviousPoseTimeStamp)
                            * SECONDS_TO_MILLI;
                    mAdf2StartPreviousPoseTimeStamp = pose.timestamp;
                    mAdf2StartTranslationTextView.setText(translationString);
                    mAdf2StartQuatTextView.setText(quaternionString);
                    mAdf2StartPoseStatusTextView.setText(getPoseStatus(pose));
                    mAdf2StartPoseCountTextView.setText(Integer.toString(mAdf2StartPoseCount));
                    mAdf2StartPoseDeltaTextView.setText(threeDec.format(mAdf2StartPoseDelta));
                    if (pose.statusCode == TangoPoseData.POSE_VALID) {
                        mIsRelocalized = true;
                        // Set the color to green
                    } else {
                        mIsRelocalized = false;
                        // Set the color blue
                    }
                }
            }
        });
    }


    private String getPoseStatus(TangoPoseData pose) {
        switch (pose.statusCode) {
            case TangoPoseData.POSE_INITIALIZING:
                return getString(R.string.pose_initializing);
            case TangoPoseData.POSE_INVALID:
                return getString(R.string.pose_invalid);
            case TangoPoseData.POSE_VALID:
                return getString(R.string.pose_valid);
            default:
                return getString(R.string.pose_unknown);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }


    // OnClick Button Listener for all the buttons
    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.first_person_button:
                Toast.makeText(getApplicationContext(), R.string.tango_error, Toast.LENGTH_SHORT)
                        .show();
//                mRenderer.setFirstPersonView();
                break;
            case R.id.top_down_button:
                Toast.makeText(getApplicationContext(), R.string.tango_error, Toast.LENGTH_SHORT)
                        .show();
//                mRenderer.setTopDownView();
                break;
            case R.id.third_person_button:
                Toast.makeText(getApplicationContext(), R.string.tango_error, Toast.LENGTH_SHORT)
                        .show();
//                mRenderer.setThirdPersonView();
                break;
            case R.id.saveAdf:
                saveAdf();
                break;
            default:
                Log.w(TAG, "Unknown button click");
                return;
        }
    }

}
