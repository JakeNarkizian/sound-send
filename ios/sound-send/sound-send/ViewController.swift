//
//  ViewController.swift
//  sound-send
//
//  Created by Jake Narkizian on 10/20/16.
//  Copyright © 2016 Jake Narkizian. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    //the base url, change it when we have one i guess?
    let baseurl = "http://www.soundsend.com"
    let createchannelpath = "/channelmanager/createchannel/"
    let channelCreateSuccessStatusCode = 201
    let channelCreateFailureStatusCode = 400
    
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
    
    //MARK: properties
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    //MARK: actions
    
}

