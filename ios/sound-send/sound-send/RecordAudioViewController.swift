//
//  RecordAudioViewController.swift
//  sound-send
//
//  Created by Aditi Gupta on 11/23/16.
//  Copyright © 2016 Aditi Gupta. All rights reserved.
//

import UIKit
import AVFoundation
import MediaPlayer
import Alamofire
var recordingSession: AVAudioSession!
var audioRecorder: AVAudioRecorder!
var innerAudioRecorder: AVAudioRecorder!
var recordingFinished: Bool! = false

class RecordAudioViewController: UIViewController {
   
    @IBOutlet weak var recordButton: UIButton!

    override func viewDidLoad() {
        super.viewDidLoad()
        recordingSession = AVAudioSession.sharedInstance()
        do {
            try recordingSession.setCategory(AVAudioSessionCategoryPlayAndRecord)
            try recordingSession.setActive(true)
            recordingSession.requestRecordPermission(){ [unowned self] allowed in
                DispatchQueue.main.async {
                    if allowed {
                        self.recordButton.backgroundColor = UIColor.blue
                        self.recordButton.setTitle("Tap to Record", for: .normal)
                        self.recordButton.addTarget(self, action: #selector(self.recordTapped), for: .touchUpInside)
                       // self.loadRecordingUI()
                    } else {
                        self.recordButton.translatesAutoresizingMaskIntoConstraints = false
                        self.recordButton.setTitle("Recording failed: please ensure the app has access to your microphone.", for: .normal)
                        self.recordButton.titleLabel?.font=UIFont.preferredFont(forTextStyle: .title1)
                        //self.loadFailUI()
                    }
                }
            }
        } catch {
            //self.loadFailUI()
        }


        // Do any additional setup after loading the view.
    }
    
    class func getDocumentsDirectory() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        let documentsDirectory = paths[0]
        return documentsDirectory
    }
    
    class func getAudioURL(i: Int) -> URL {
        //var audioString = "audio" + String(arc4random()) + ".m4a"
        let audioString = String(i) + ".m4a"
        return getDocumentsDirectory().appendingPathComponent(audioString)
    }
    
    func spawnRecording(i:Int){
        view.backgroundColor = UIColor(red: 0.6, green: 0, blue: 0, alpha: 1)
        recordingFinished = false
        recordButton.setTitle("Tap to Stop", for: .normal)
        recordButton.setNeedsDisplay()
        
        let audioURL = RecordAudioViewController.getAudioURL(i:i)
        backgroundThread(background: {
            do {
                print(audioURL.absoluteString)
                let settings = [
                    AVFormatIDKey: Int (kAudioFormatMPEG4AAC),
                    AVSampleRateKey: 12000,
                    AVNumberOfChannelsKey: 2,
                    AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
                ]
                audioRecorder = try AVAudioRecorder(url: audioURL, settings: settings)
                print ("an instance of audiorecorder has been created")
                //audioRecorder.delegate = self
                print ("my delegate is myself")
                audioRecorder.record(forDuration: 10)
                print ("i am now recording")
                
                sleep(10)
                if (audioRecorder != nil) {
                    audioRecorder.stop()
                    audioRecorder = nil
                }
            }
            catch {
                // do something
            }
        }, completion: {
            if recordingFinished! != true { self.spawnRecording(i: i+1) }
            self.postRecording(audioURL: audioURL)
        })
    }
    
    func backgroundThread(delay: Double = 0.0, background: (() -> Void)? = nil, completion: (() -> Void)? = nil) {
        DispatchQueue.global(qos: .userInitiated).async {
            if(background != nil){ background!(); }
            
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now(), execute: { if(completion != nil) {completion!()} })
        }
    }
    
    func postRecording(audioURL: URL) {
        /*Alamofire.upload(
         to: "http://127.0.0.1/5000",
         method: .POST,
         headers: ["Authorization" : "Basic xxx"],
         multipartFormData: { multipartFormData in
         multipartFormData.appendBodyPart(fileUrl: audioURL, name: "photo")
         },
         encodingCompletion: { encodingResult in
         switch encodingResult {
         case .Success(let upload, _, _):
         upload.responseJSON { request, response, JSON, error in
         
         
         }
         case .Failure(let encodingError): break
         
         }
         }
         )*/
        Alamofire.upload(audioURL, to:"http://127.0.0.1/5000").responseJSON { response in
            debugPrint(response)
        }
    }

    
    func recordTapped() {
        if audioRecorder == nil {
            spawnRecording(i: 1)
        }
        else {
            recordingFinished = true
            view.backgroundColor = UIColor(red: 0, green: 0.6, blue: 0, alpha: 1)
            self.recordButton.backgroundColor = UIColor.blue
            self.recordButton.setTitle("Done!", for: .normal)
        }

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
