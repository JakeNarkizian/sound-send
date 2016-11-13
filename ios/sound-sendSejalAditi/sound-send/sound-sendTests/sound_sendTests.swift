//
//  sound_sendTests.swift
//  sound-sendTests
//
//  Created by Aditi Gupta on 11/1/16.
//  Copyright © 2016 Aditi Gupta. All rights reserved.
//

import XCTest
import Nocilla
@testable import sound_send


class sound_sendTests: XCTestCase {
    
    //var expectation: XCTestExpectation!
    
    override class func setUp() {
        super.setUp()
        
        //LSNocilla.sharedInstance().start()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override class func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
        //LSNocilla.sharedInstance().stop()
    }
    
    override func setUp() {
        super.setUp()
        //expectation = expectationWithDescription("")
    }
    
    override func tearDown() {
        super.tearDown()
       // expectation = nil
        //LSNocilla.sharedInstance().clearStubs()
    }
    
    func testExample() {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        /*let dataViewController = DataViewController()
        let dataViewControllerResponse = dataViewController.makeHTTPcall("http://www.google.com")
        XCTAssert(dataViewControllerResponse == 200)*/
        //stubRequest("GET", "http://www.google.com");
        //XCTAssert(
        
    }
    
    func testPerformanceExample() {
        // This is an example of a performance test case.
        self.measureBlock {
            // Put the code you want to measure the time of here.
        }
    }
    
}
