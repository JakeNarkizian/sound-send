//
//  ViewController.swift
//  sound-send
//
//  Created by Jake Narkizian on 10/20/16.
//  Copyright © 2016 Jake Narkizian. All rights reserved.
//

import UIKit
import AVFoundation

class PlayChannelViewController: UIViewController {
    //the base url, change it when we have one i guess?
    let baseurl = "http://127.0.0.1:5000"
    let createchannelpath = "/channelmanager/create/"
    let chunkpath = "/segs/"
    let indexpath = "/"
    let channelCreateSuccessStatusCode = 201
    let channelCreateFailureStatusCode = 400
    var players: [AVAudioPlayer?]=[]
    var currentaudio: [Data?] = []
    var downloadedSoundEnds:TimeInterval? = nil
    var latestPlayed:Int? = nil
    var stillPlaying = true
    var channelname:String = "insertchannelnamehere"
    
    func generateCreateChannelURL(channelname: String) -> String {
        let uuid = UIDevice.current.identifierForVendor!.uuidString
        return baseurl+createchannelpath+channelname+"/"+uuid
    }
    
    //sends a create channel get request with an input channel name
    func createChannel(channelname: String) {
        let url = NSURL(string: generateCreateChannelURL(channelname: channelname))
        
        let task = URLSession.shared.dataTask(with: url! as URL) {(data, response, error) in
            self.handleCreateChannelResponse(data: data, response: response, error: error)
        }
        
        task.resume()
    }
    
    //creates an alert with the title "Error" and an input string
    func showAlert(alertstring: String) {
        let alertController = UIAlertController(title: "Error", message: alertstring, preferredStyle: UIAlertControllerStyle.alert)
        let okAction = UIAlertAction(title: "OK", style: UIAlertActionStyle.default) { (result : UIAlertAction) -> Void in
            //do nothing just close the alert
        }
        alertController.addAction(okAction)
        self.present(alertController, animated: true, completion: nil)
    }
    
    //takes a create channel response and shows alerts if something's wrong. also resets session in progress if there's an error
    func handleCreateChannelResponse(data: Data?, response: URLResponse?, error: Error?) {
        if(error != nil) {
            //make an alert with the error
            showAlert(alertstring: error!.localizedDescription)
        }
        if (response != nil) {
            //need to do this to have access to the status code
            let httpresponse = response as! HTTPURLResponse
            //take the status code and show an alert if needed
            let alert = handleCreateChannelResponseCode(statuscode: httpresponse.statusCode)
            if (alert != nil) {
                showAlert(alertstring: alert!)
            }
        }
        if (data != nil) {
            //if there is anything that needs data it can go here
        }
    }
    
    //takes the status code from the create channel response and interpret it
    func handleCreateChannelResponseCode(statuscode:Int) -> String? {
        var message:String? = nil
        if(statuscode != channelCreateSuccessStatusCode) {
            if (statuscode == channelCreateFailureStatusCode) {
                message = "Channel name invalid. There may already be a channel with that name."
            }
            else {
                message = "Status code: " + String(statuscode)
            }
        }
        return message
    }
    
    //takes a sound (as a Data object) and plays it, with a delay if something is already playing
    //so its like a queue
    func playSound(sound:Data) {
        do {
            players.append(try AVAudioPlayer(data: sound, fileTypeHint: "m4a"))
            guard let player = players[players.count-1] else { return }
            if (downloadedSoundEnds == nil) {
                print(player.deviceCurrentTime)
                
                downloadedSoundEnds = player.deviceCurrentTime + player.duration
                player.prepareToPlay()
                player.play()
            }
            else if (downloadedSoundEnds!<player.deviceCurrentTime){
                downloadedSoundEnds = player.deviceCurrentTime + player.duration
                player.prepareToPlay()
                player.play()
            }
            else {
                player.prepareToPlay()
                player.play(atTime: downloadedSoundEnds!)
                downloadedSoundEnds! += player.duration
            }
        } catch let error {
            print(error.localizedDescription)
        }
    }
    
    func generateIndexURL(channelname: String) -> String {
        return baseurl + indexpath + channelname + "/" + "index.json"
    }
    
    func getChunk(urlstring: String) {
        //let url = NSURL(string: generateGetChunkURL(channelname: channelname, currentchunk: currentchunk))
        let url = NSURL(string: urlstring)
        let task = URLSession.shared.dataTask(with: url! as URL) {(data, response, error) in
            self.handleGetChunkResponse(data: data, response: response, error: error)
        }
        
        task.resume()
    }
    
    
    func handleGetIndexResponse(data: Data?, response: URLResponse?, error: Error?, channelname: String) {
        if(error != nil) {
            //make an alert with the error
            showAlert(alertstring: error!.localizedDescription)
        }
        if (response != nil) {
            //need to do this to have access to the status code
            let httpresponse = response as! HTTPURLResponse
            //take the status code and show an alert if needed
            let alert = handleCreateChannelResponseCode(statuscode: httpresponse.statusCode)
            if (alert != nil) {
                //showAlert(alertstring: alert!)
            }
        }
        if (data != nil) {
            //let urls = processIndexFile(data: String(data: data!, encoding: String.Encoding.utf8)!)
            
            if let json = try? JSONSerialization.jsonObject(with: data!, options: []) as? [String: AnyObject] {
                let chunk = json?["current"] as! Int
                let nexttoplay = getNextChunk(chunk: chunk)
                if (nexttoplay != nil) {
                    latestPlayed = nexttoplay
                    let url = ((json?["url"] as! NSString) as String) + String(nexttoplay!) + ((json?["format"] as! NSString) as String)
                    getChunk(urlstring: url)
                }
                
            }
        }
    }
    
    //parse the index file into an array of strings
    /*func processIndexFile(data:String) -> [String] {
        return []
    }*/
    
    func handleGetChunkResponse(data: Data?, response: URLResponse?, error: Error?) {
        if(error != nil) {
            //make an alert with the error
            showAlert(alertstring: error!.localizedDescription)
        }
        if (response != nil) {
            //need to do this to have access to the status code
            let httpresponse = response as! HTTPURLResponse
            //take the status code and show an alert if needed
            let alert = handleCreateChannelResponseCode(statuscode: httpresponse.statusCode)
            if (alert != nil) {
                //showAlert(alertstring: alert!)
            }
        }
        if (data != nil) {
            playSound(sound: data!)
        }
    }
    
    //with the latest urls parse, find the next url to play
    func getNextChunk(chunk:Int) -> Int? {
        if (latestPlayed == nil) {
            return chunk
        }
        else {
            if (chunk == latestPlayed) {
                return nil
            }
            return chunk + 1
        }
    }
    
    func stopSounds() {
        print("hi")
        for player in players {
            player!.stop()
        }
        stillPlaying = false
    }
    
    func backgroundThread(delay: Double = 0.0, background: (() -> Void)? = nil, completion: (() -> Void)? = nil) {
        DispatchQueue.global(qos: .userInitiated).async {
            if(background != nil){ background!(); }
            
            DispatchQueue.main.asyncAfter(deadline: DispatchTime.now(), execute: { if(completion != nil) {completion!()} })
        }
    }
    
    
    func makeNewIndexRequest() {
        backgroundThread(background: {
            let url = NSURL(string: self.generateIndexURL(channelname: self.channelname))
            
            let task = URLSession.shared.dataTask(with: url! as URL) {(data, response, error) in
                self.handleGetIndexResponse(data: data, response: response, error: error, channelname: self.channelname)
            }
            
            task.resume()
            sleep(1)
            }, completion: {
                if (self.stillPlaying) {
                    self.makeNewIndexRequest()
                    print("playing")
                }
                else {
                    print("done playing")
                }
            }
        )
    }
    
    
    //MARK: properties
    
    /*func getdata(filename:String) -> Data {
        let url = Bundle.main.path(forResource: filename, ofType:"mp3")
        return NSData(contentsOfFile:url!) as! Data
    }*/
    
    override func viewDidLoad() {
        super.viewDidLoad()
        makeNewIndexRequest()
    }

    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    //MARK: actions
    
    @IBAction func stopButtonPressed(_ sender: AnyObject) {
        stopSounds()
    }
}

