#=======================================================================
# verilog_parser
#=======================================================================

import pytest
import os

from verilog_parser import header_parser

#-----------------------------------------------------------------------
# test cases
#-----------------------------------------------------------------------

def a(): return """\
module tester;
endmodule
"""

def b(): return """\
module vc_QueueCtrl1
(
  input  clk, reset,
  input  enq_val,
  output enq_rdy,
  output deq_val,
  input  deq_rdy,
  output wen,
  output bypass_mux_sel
);
endmodule
"""

def c(): return """\
module vc_QueueCtrl1
(
  input  clk, reset,
  input  enq_val,
  output reg enq_rdy,
  output reg deq_val,
  input  deq_rdy,
  output reg wen,
  output bypass_mux_sel
);
endmodule
"""

def d(): return """\
module vc_QueueCtrl1
(
  input  [0  :0] clk, reset,
  input  [1  :0] enq_val,
  output [0  :0] enq_rdy,
  output [4  :0] deq_val,
  input  [0  :0] deq_rdy,
  output [0  :0] wen,
  output [2-1:0] bypass_mux_sel
);
endmodule
"""

def e(): return """\
//module vc_QueueCtrl1 #( parameter TYPE = `VC_QUEUE_NORMAL )
module vc_QueueCtrl1 //#( parameter TYPE = `VC_QUEUE_NORMAL )
(
  input  clk, reset,
  input  enq_val,        // Enqueue data is valid
  output enq_rdy,        // Ready for producer to do an enqueue
  output deq_val,        // Dequeue data is valid
  input  deq_rdy,        // Consumer is ready to do a dequeue
  output wen,            // Write en signal to wire up to storage element
  output bypass_mux_sel  // Used to control bypass mux for bypass queues
);
endmodule
"""

def f(): return """\
module vc_QueueCtrl1 #( parameter TYPE = `VC_QUEUE_NORMAL )
(
  input  clk, reset,
  input  enq_val,        // Enqueue data is valid
  output enq_rdy,        // Ready for producer to do an enqueue
  output deq_val,        // Dequeue data is valid
  input  deq_rdy,        // Consumer is ready to do a dequeue
  output wen,            // Write en signal to wire up to storage element
  output bypass_mux_sel  // Used to control bypass mux for bypass queues
);
endmodule
"""

def g(): return """\
// comment
module simple /* comment */
(
  input  in, // comment
  /* comment */
  output out // comment
);
endmodule
"""

def h(): return """\
  module vc_RoundRobinArbChain
  #(
    parameter NUM_REQS           = 2,
    parameter RESET_PRIORITY_VAL = 1  // (one-hot) 1 indicates which req
                                      //   has highest priority on reset
  )(
    input                 clk,
    input                 reset,
    input                 kin,    // Kill in
    input  [NUM_REQS-1:0] reqs,   // 1 = making a request, 0 = no request
    output [NUM_REQS-1:0] grants, // (one-hot) 1 is req won grant
    output                kout    // Kill out
  );
  endmodule
"""

def i(): return """\
  module mod_a #( parameter a = 2, parameter b = 3 )
  (
    input  in,
    output out
  );
  endmodule
"""

def j(): return """\
  module mod_a
  #( parameter a = 2 )
  (
    input  in,
    output out
  );
  endmodule

  module mod_b
  #( parameter a = 2, parameter b = 2)
  (
    input  in,
    output out
  );
  endmodule
"""

def k(): return """\
  `ifdef SOMETHING
  `define SOMETHING
  module mod_a
  #( parameter a = 2 )
  (
    input  in,
    output out
  );
  endmodule
  //`endif
"""
def l(): return """\
  `ifdef SOMETHING
  `define SOMETHING
  module mod_a
  #( parameter a = 2 )
  (
    input  in,
    output out
  );
  endmodule
  module mod_b
  #( parameter a = 2 )
  (
    input  in,
    output out
  );
  endmodule
  //`endif
"""

def m(): return """\
module vc_MemPortWidthAdapter
#(
  parameter p_addr_sz = 32,
  parameter p_proc_data_sz = 32,
  //parameter p_mem_data_sz = 128

  // Local constants not meant to be set from outside the module
  //parameter c_proc_req_msg_sz  = `VC_MEM_REQ_MSG_SZ(p_addr_sz,p_proc_data_sz),
  parameter c_proc_resp_msg_sz = `VC_MEM_RESP_MSG_SZ(p_proc_data_sz)
)(
  input  [c_proc_req_msg_sz-1:0]  procreq_msg,
  output [c_proc_resp_msg_sz-1:0] procresp_msg
);
endmodule
"""

def n(): return """\
module vc_TraceWithValRdy
#(
  parameter integer NUMBITS      = 1,
  parameter integer FORMAT_CHARS = 2,
  parameter [(FORMAT_CHARS<<3)-1:0] FORMAT = "%x"
)(
  input  [(NUMCHARS<<3)-1:0] istr,
  input  [NUMBITS-1:0]       bits
);
endmodule
"""

def y(): return """\
module fulladder ( carry, sum, in1, in2, in3 );
endmodule
"""

def x(): return """\
module fulladder ( carry, sum, in1, in2, in3 );
  input in1, in2, in3;
  output carry, sum;
  //xor U5 ( in1, n3, sum );
endmodule
"""

#-----------------------------------------------------------------------
# test_simple
#-----------------------------------------------------------------------
@pytest.mark.parametrize( 'src',
  [a, b, c, d, e, f, g, h, i, j, k, l, m, n, y, x]
)
def test_simple( src ):
  parser = header_parser()
  parser.parseString( src(), parseAll=True )

#-----------------------------------------------------------------------
# test_simple
#-----------------------------------------------------------------------
home  = os.path.expanduser('~')
path  = '{}/vc/git-brg/pyparc/vc'.format(home)

if os.path.exists( path ):
  files = os.listdir( path )
  files = ( x for x in files if not x.endswith('.t.v' ) and x.endswith('.v') )
  files = [ os.path.join( path, x ) for x in files ]
else:
  files = []

@pytest.mark.parametrize( 'filename', files )
def test_files( filename ):

  parser = header_parser()
  print filename
  parser.parseFile( filename )




