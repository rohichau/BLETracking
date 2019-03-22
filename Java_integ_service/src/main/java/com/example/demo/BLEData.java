package com.example.demo;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({"address", "addType","rssi","logTime"})
public class BLEData {
	
	@JsonProperty("address")
	String address;
	@JsonProperty("rssi")
	double rssi;
	
	public String getAddress() {
		return address;
	}
	public void setAddress(String address) {
		this.address = address;
	}

	/*
	 * public String getAddType() { return addType; } public void setAddType(String
	 * addType) { this.addType = addType; }
	 */
	public double getRssi() {
		return rssi;
	}
	public void setRssi(double rssi) {
		this.rssi = rssi;
	}
	public String getEpochTime() {
		return epochTime;
	}
	public void setEpochTime(String epochTime) {
		this.epochTime = epochTime;
	}
}
