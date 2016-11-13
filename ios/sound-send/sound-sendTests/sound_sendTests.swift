//
//  sound_sendTests.swift
//  sound-sendTests
//
//  Created by Aditi Gupta on 11/23/16.
//  Copyright © 2016 Aditi Gupta. All rights reserved.
//

import XCTest
@testable import sound_send

class sound_sendTests: XCTestCase {
    
    var vc: ViewController!
    
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle.main)
        vc = storyboard.instantiateInitialViewController() as! ViewController
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testGenerateCreateChannelURL() {
        let url = vc.generateCreateChannelURL(channelname: "test")
        let uuid = UIDevice.current.identifierForVendor!.uuidString
        XCTAssert(url == (vc.baseurl+vc.createchannelpath+"test/"+uuid))
    }
    
    func testHandleCreateChannelResponseCode() {
        let goodcode = vc.channelCreateSuccessStatusCode
        XCTAssert(vc.handleCreateChannelResponseCode(statuscode: goodcode) == nil)
        let badcode = vc.channelCreateFailureStatusCode
        XCTAssert(vc.handleCreateChannelResponseCode(statuscode: badcode) != nil)
    }

    
}
