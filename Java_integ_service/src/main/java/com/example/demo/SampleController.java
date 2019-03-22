package com.example.demo;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SampleController {

	@PostMapping(path = "/postIt", consumes = MediaType.APPLICATION_JSON_VALUE)
	public void receiveBleSignal(@RequestBody BLEData bleRequest) {

		System.out.printf("READING THE REQUST: Address : %s rssi: %f Timestamp: %s \n", bleRequest.address,
				bleRequest.rssi);

	}

}
