//
//  connect.swift
//  sound-send
//

import Foundation

class connect {
    init() {
        
    }
    
    func connectToServer() {
        let url:NSURL = NSURL(string: "https://stackoverflow.com")!
        let session = NSURLSession.sharedSession()
    
        let request = NSMutableURLRequest(URL: url)
        request.HTTPMethod = "POST"
        request.cachePolicy = NSURLRequestCachePolicy.ReloadIgnoringCacheData
        
        let paramString = "data=Hello"
        request.HTTPBody = paramString.dataUsingEncoding(NSUTF8StringEncoding)
        
        let task = session.dataTaskWithRequest(request) {
            (let data, let response, let error) in
            guard let _:NSData = data, let _:NSURLResponse = response
                where error == nil else {
                    print("error")
                    return
                }
            
            let dataString = NSString(data: data!, encoding: NSUTF8StringEncoding)
            print(dataString)
        }
        task.resume()
    }
    
}