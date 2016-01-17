package com.github.rombolab.android_rostango.tangoarealearning;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.widget.ToggleButton;


import com.google.atap.tangoservice.Tango;


public class ALStartActivity extends Activity implements View.OnClickListener  {


    public static final String USE_AREA_LEARNING =
            "com.rombolab.android_rostango.tangoarealearning.usearealearning";
    public static final String LOAD_ADF = "com.rombolab.android_rostango.tangoarealearning.loadadf";
    public static final String LOAD_GRAPHICS = "com.rombolab.android_rostango.tangoarealearning.loadgraphics";
    private ToggleButton mLearningModeToggleButton;
    private ToggleButton mLoadADFToggleButton;
    private ToggleButton mLoadGraphicsToggleButton;
    private Button mStartButton;
    private boolean mIsUseAreaLearning;
    private boolean mIsLoadADF;
    private boolean mIsLoadGraphics;

/*    public AreaLearningStartActivity() {
        super("AreaLearning", "AreaLearning");
    }
*/

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.start_activity);
        setTitle(R.string.app_name);
        mLearningModeToggleButton = (ToggleButton) findViewById(R.id.learningmode);
        mLoadADFToggleButton = (ToggleButton) findViewById(R.id.loadadf);
        mStartButton = (Button) findViewById(R.id.start);
        mLoadGraphicsToggleButton = (ToggleButton) findViewById(R.id.loadgraphics);
        mStartButton.setOnClickListener(this);
        findViewById(R.id.ADFListView).setOnClickListener(this);
        mLearningModeToggleButton.setOnClickListener(this);
        mLoadADFToggleButton.setOnClickListener(this);

      //  startActivityForResult(
       //         Tango.getRequestPermissionIntent(Tango.PERMISSIONTYPE_MOTION_TRACKING), 0);

        startActivityForResult(
                Tango.getRequestPermissionIntent(Tango.PERMISSIONTYPE_ADF_LOAD_SAVE), 0);
    }






    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.loadadf:
                mIsLoadADF = mLoadADFToggleButton.isChecked();
                break;
            case R.id.loadgraphics:
                mIsLoadGraphics = mLoadGraphicsToggleButton.isChecked();
                break;
            case R.id.learningmode:
                mIsUseAreaLearning = mLearningModeToggleButton.isChecked();
                break;
            case R.id.start:
                startAreaDescriptionActivity();
                break;
            case R.id.ADFListView:
                startADFListView();
                break;
        }
    }


    private void startAreaDescriptionActivity() {
        Intent startADIntent = new Intent(this, AreaLearningActivity.class);
        mIsUseAreaLearning = mLearningModeToggleButton.isChecked();
        mIsLoadADF = mLoadADFToggleButton.isChecked();
        mIsLoadGraphics =mLoadGraphicsToggleButton.isChecked();

        startADIntent.putExtra(USE_AREA_LEARNING, mIsUseAreaLearning);
        startADIntent.putExtra(LOAD_ADF, mIsLoadADF);
        startADIntent.putExtra(LOAD_GRAPHICS, mIsLoadGraphics);
        startActivity(startADIntent);
    }

    private void startADFListView() {
        Intent startADFListViewIntent = new Intent(this, ADFUUIDListViewActivity.class);
        startActivity(startADFListViewIntent);

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // Check which request we're responding to
//        if (requestCode == 0) {
//            // Make sure the request was successful
//            if (resultCode == RESULT_CANCELED) {
//                Toast.makeText(this, R.string.motiontracking_permission, Toast.LENGTH_SHORT).show();
//                finish();
//            }
//        } else
          if (requestCode == 0) {
            // Make sure the request was successful
            if (resultCode == RESULT_CANCELED) {
                Toast.makeText(this, R.string.arealearning_permission, Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }

}










