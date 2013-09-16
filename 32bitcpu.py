#coding:utf-8
from myhdl import Signal,intbv, delay, instance,instances, always,now,Simulation,traceSignals,toVerilog
import random

#24-31 is not use
#16-23 is opcode
#8-15 is ope1
#0-7 is ope2
#xxxxxxxx b00000001 xxxxxxxxx xxxxxxx:add
#xxxxxxxx b00000010 xxxxxxxxx xxxxxxx:sub
#xxxxxxxx b00000011 xxxxxxxxx xxxxxxx:mul
#xxxxxxxx b00000100 xxxxxxxxx xxxxxxx:div
#xxxxxxxx b00000101 xxxxxxxxx xxxxxxx:rem

clock=Signal(bool(1))
insn_in=Signal(intbv(0)[32:])
insn_out=Signal(intbv(0)[32:])
opcode=Signal(intbv(0)[8:])
ope1=Signal(intbv(0)[8:])
ope2=Signal(intbv(0)[8:])
result=Signal(intbv(0)[8:])

def fetch(clock,insn_in,insn_out):
    @always(clock.posedge)
    def proc():
        insn_out.next=insn_in
    return proc

def decode(clock,insn_out,opcode,ope1,ope2):
    @always(clock.posedge)
    def proc():
        opcode.next=insn_out[24:16]
        ope1.next=insn_out[16:8]
        ope2.next=insn_out[8:0]
    return proc

def execution(clock,opcode,ope1,ope2,result):
    @always(clock.posedge)
    def proc():
        if(opcode==1):#add
            result.next=ope1+ope2
        elif(opcode==2):#sub
            result.next=ope1-ope2
        elif(opcode==3):#mul
            result.next=ope1*ope2
        elif(opcode==4):#div
            result.next=ope1//ope2
        elif(opcode==5):#rem
            result.next=ope1%ope2

    return proc

def writeback(clock,result):
    @always(clock.posedge)
    def proc():
        pass
    return proc

#toVerilog(fetch,clock,insn_in,insn_out)
#toVerilog(decode,clock,insn_out,opcode,ope1,ope2)
#toVerilog(execution,clock,opcode,ope1,ope2,result)
#toVerilog(writeback,clock,result)

def test_nr():

    fe=fetch(clock,insn_in,insn_out)
    deco=decode(clock,insn_out,opcode,ope1,ope2)
    execu=execution(clock,opcode,ope1,ope2,result)
    writeb=writeback(clock,result)

    @always(delay(10))
    def driveClk():
        clock.next=not clock
    @instance
    def stimulus():
        while True:
            yield clock.posedge
            #                                 mul                3             3
            insn_in.next=0b0000000<<24 | 0b000000011<<16 | 0b00000011<<8 | 0b00000011
            print "%s,%s,%x,%s"%(clock,now(),insn_in,result)
    return instances()
th=traceSignals(test_nr)
sim=Simulation(th)
sim.run(100)
