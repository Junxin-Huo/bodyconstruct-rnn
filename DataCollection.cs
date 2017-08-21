using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class DataCollection : MonoBehaviour {
    string file_name = "data.txt";

    [SerializeField]
    Transform FollowCamera;

    [SerializeField]
    Transform RightHand;
    [SerializeField]
    Transform LeftHand;
    [SerializeField]
    Transform FollowRightHand;
    [SerializeField]
    Transform FollowLeftHand;

    [SerializeField]
    TextMesh text;

    FileStream fs;
    StreamWriter sw;
    bool writing = false;
    int writeCount = 0;
    int writeFrame = 0;

	void Start () {
        if (!AddChildren(FollowRightHand))
        {
            Debug.Log("Initial error!");
        }

	}
	
	void Update () {
        MyFollow();

        bool triggerClicked = false;
		if (OVRInput.GetUp(OVRInput.RawButton.RIndexTrigger))
        {
            Debug.Log("RIndexTrigger Up");
            triggerClicked = true;
        }

        if (!writing && triggerClicked)     //start writing
        {
            Debug.Log("Start writing ............................(count:" + writeCount + ")");
            text.text = "Start writing ............................(count:" + writeCount + ")";
            writing = true;
            triggerClicked = false;
            writeCount++;
            if (File.Exists(file_name))
                fs = new FileStream(file_name, FileMode.Append);
            else
                fs = new FileStream(file_name, FileMode.Create);
            sw = new StreamWriter(fs);
        }
        else if (writing && !triggerClicked)       //writing file
        {
            writeFrame++;
            sw.Write("Frame:" + writeFrame + "\n");
            text.text = "Frame: " + writeFrame;
            sw.Write("RH " + WritePositionAdvanceAngle(FollowRightHand));
            sw.Write("RE " + WritePositionEulerAngle(FollowLeftHand));
            sw.Write("CA " + WritePositionEulerAngle(Camera.main.transform));
            sw.Flush();
        }
        else if (writing && triggerClicked)         //stop writing
        {
            Debug.Log("End writing ............................");
            text.text = "End writing ............................";
            writeFrame = 0;
            writing = false;
            triggerClicked = false;
            sw.Close();
            fs.Close();
        }
	}

    bool AddChildren(Transform tran)
    {
        if (tran == null)
        {
            Debug.Log("tran is null");
            return false;
        }

        GameObject ObjZ = GameObject.CreatePrimitive(PrimitiveType.Cube);
        ObjZ.transform.parent = tran;
        ObjZ.transform.localPosition = new Vector3(0f, 0f, 1f);
        ObjZ.transform.localScale = new Vector3(0.3f, 0.3f, 0.3f);
        ObjZ.name = tran.gameObject.name + "'s child_z";

        GameObject ObjY = GameObject.CreatePrimitive(PrimitiveType.Cube);
        ObjY.transform.parent = tran;
        ObjY.transform.localPosition = new Vector3(0f, 1f, 0f);
        ObjY.transform.localScale = new Vector3(0.3f, 0.3f, 0.3f);
        ObjY.name = tran.gameObject.name + "'s child_y";

        return true;
    }

    void MyFollow()
    {
        Vector3 headPos = Camera.main.transform.position;
        Vector3 headRot = Camera.main.transform.eulerAngles;
        FollowCamera.position = headPos;                          //move with camera(head)
        FollowCamera.eulerAngles = new Vector3(0, headRot.y, 0);

        FollowRightHand.position = RightHand.position;
        FollowRightHand.eulerAngles = RightHand.eulerAngles;

        FollowLeftHand.position = LeftHand.position;
        FollowLeftHand.eulerAngles = LeftHand.eulerAngles;
    }

    string WritePositionEulerAngle(Transform tran)
    {
        string pos = tran.localPosition.x + " " + tran.localPosition.y + " " + tran.localPosition.z + " ";
        string rot = tran.localEulerAngles.x + " " + tran.localEulerAngles.y + " " + tran.localEulerAngles.z;
        return pos + rot + "\n";
    }

    string WritePositionAdvanceAngle(Transform tran)
    {
        Transform TranZ = tran.FindChild(tran.gameObject.name + "'s child_z");
        Transform TranY = tran.FindChild(tran.gameObject.name + "'s child_y");
        string pos = tran.localPosition.x + " " + tran.localPosition.y + " " + tran.localPosition.z + " ";
        string rot = TranZ.position.x + " " + TranZ.position.y + " " + TranZ.position.z + " "
                   + TranY.position.x + " " + TranY.position.y + " " + TranY.position.z;
        return pos + rot + "\n";
    }
}
