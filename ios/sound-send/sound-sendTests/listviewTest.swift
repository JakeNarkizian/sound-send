//
//  listviewTest.swift
//  Sound-Send3.0
//
//  Created by Sean Torres on 11/17/16.

import XCTest
@testable import sound_send//moodule
class listviewTest: XCTestCase {
    var vc:TableFillViewController!
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle.main)
        vc = storyboard.instantiateInitialViewController() as! TableFillViewController
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testZeroActiveChannels() {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        let num = vc.arr.count
        XCTAssert(num == 0)
    }
    
    func testTwoActiveChannels() {
        let myURL: String = "http://127.0.0.1:5000/channelmanager/create/apple200/12345"
        let myURL2: String = "http://127.0.0.1:5000/channelmanager/create/apple400/12345"
        let myURL3: String = "http://127.0.0.1:5000/channelmanager/active"
        vc.makeHTTPCall(requestURL: myURL)
        vc.makeHTTPCall(requestURL: myURL2)
        vc.makeHTTPCall(requestURL: myURL3)
        vc.tableView = UITableView()
        
        DispatchQueue.main.asyncAfter(deadline:DispatchTime.now() + .milliseconds(1500)) {
            print("WAITED 5 SECONDS")
            let num = self.vc!.arr.count
            print("Number: \(num)")
            print("ARRAY: \(self.vc!.arr)")
            XCTAssert(num == 2)
        }
    }
    
    func testThreeActiveChannels() {
        vc.arr = ["1", "2", "3"]
        let num = vc.arr.count
        XCTAssert(num == 3)
    }
    
    // BLACK BOX TEST (relys on server and client)
    func testforallactivelistners () {
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle.main)
        vc = storyboard.instantiateInitialViewController() as! TableFillViewController
        vc.tableView = UITableView()
        vc.arr = ["1", "2", "3"]
        vc.tableView.reloadData()
        
        print("ROWS: \(vc.tableView.numberOfRows(inSection: 0)))")
        XCTAssert(vc.tableView.numberOfSections == 3)
    }
    
}

