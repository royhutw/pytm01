#!/usr/bin/env python3

from pytm.pytm import TM, Server, ExternalEntity, Dataflow, Boundary, Actor, Data

tm = TM("Cloud VMs for development")
tm.description = "How I use cloud VMs for development"
tm.isOrdered = True

Laptop = Boundary("Laptop")
AWS = Boundary("AWS")

user = Actor("User")
user.inBoundary = Laptop

vm = Server("EC2 VM")
vm.OS = "Ubuntu"
vm.isHardened = True
vm.inBoundary = AWS
vm.onAWS = True

sg = ExternalEntity("Security Group")
sg.inBoundary = AWS

allow_ip = Dataflow(user, sg, "User allows access from own IP address")
allow_ip.protocol = "AWS API"
allow_ip.data = Data("User IP address")

start_vm = Dataflow(user, vm, "User starts EC2 instance")
start_vm.protocol = "AWS API"

read_vm_dns = Dataflow(vm, user, "User reads DNS name of EC2 instance")
read_vm_dns.protocol = "AWS API"

use_vm = Dataflow(user, vm, "User uses VM")
use_vm.protocol = "SSH"
use_vm.data = "Development commands and data"
use_vm.dstPort = 22

stop_vm = Dataflow(user, vm, "User stops VM")
stop_vm.protocol = "AWS API"

tm.process()