//
//  DataViewController.swift
//  sound-send
//
//  Created by Aditi Gupta on 11/1/16.
//  Copyright © 2016 Aditi Gupta. All rights reserved.
//

import UIKit

class DataViewController: UIViewController {

    @IBOutlet weak var dataLabel: UILabel!
    var dataObject: String = ""

    @IBOutlet weak var channelNameTxtField: UITextField!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        //self.dataLabel!.text = dataObject
    }
    
    //http://swiftdeveloperblog.com/http-get-request-example-in-swift/
    @IBAction func sendButtonPressed(sender: AnyObject) {
        let channelNameValue = channelNameTxtField.text
        
        if isStringEmpty(channelNameValue!) {
            return
        }
        
        //Send HTTP Get Request
        
        //Server Side URL
        let scriptUrl = "http://www.google.com"
        makeHTTPcall(scriptUrl)
        
    }
    
    //func makeHTTPcall(let scriptUrl: String) -> NSString {
    func makeHTTPcall (let scriptUrl: String) {
        //Enter Channel Name
        //let urlWithParams = scriptUrl + "?channelName=\(channelNameValue!)"
        
        //Create NSURL Object
        //let myUrl = NSURL(string: urlWithParams);
        let myUrl = NSURL(string: scriptUrl);
        
        //Create URL Request
        let request = NSMutableURLRequest(URL:myUrl!);
        
        //set request HTTP method to GET. It could be POST as well
        request.HTTPMethod = "GET"
        
        
        //Execute HTTP Request
        //var responseString: NSString = ""
        let task = NSURLSession.sharedSession().dataTaskWithRequest(request) {
            data, response, error in
            
            //check for error
            if error != nil
            {
                print("error=\(error)")
               // return
            }
            
            //print out response string
            //responseString = NSString(data: data!, encoding: NSUTF8StringEncoding)!
            //print("responseString=\(responseString)")
            
        }
        
        task.resume() 
        //return responseString
    }
    
    //Makes sure user has entered a valid value. Also checks for case where the user may have submitted empty spaces
    func isStringEmpty(var stringValue: String) -> Bool {
        if stringValue.isEmpty
        {
            return true
        }
        
        stringValue = stringValue.stringByTrimmingCharactersInSet(NSCharacterSet.whitespaceCharacterSet())
        
        if(stringValue.isEmpty == true)
        {
            return true
        }
        
        return false
    }
    
    


}

