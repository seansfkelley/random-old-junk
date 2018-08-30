	.section	__TEXT,__text,regular,pure_instructions
	.section	__TEXT,__StaticInit,regular,pure_instructions
	.align	4, 0x90
__GLOBAL__I___classnames:
Leh_func_begin1:
	pushq	%rbp
Ltmp0:
	movq	%rsp, %rbp
Ltmp1:
	movl	$1, %eax
	movl	$65535, %ecx
	movl	%eax, %edi
	movl	%ecx, %esi
	callq	__Z41__static_initialization_and_destruction_0ii
	popq	%rbp
	ret
Leh_func_end1:

	.section	__TEXT,__textcoal_nt,coalesced,pure_instructions
	.globl	__ZNKSt9type_info4nameEv
.weak_definition __ZNKSt9type_info4nameEv
	.align	1, 0x90
__ZNKSt9type_info4nameEv:
Leh_func_begin2:
	pushq	%rbp
Ltmp2:
	movq	%rsp, %rbp
Ltmp3:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, -16(%rbp)
	movq	-16(%rbp), %rax
	popq	%rbp
	ret
Leh_func_end2:

	.globl	__ZN4BaseC2Ev
.weak_definition __ZN4BaseC2Ev
	.align	1, 0x90
__ZN4BaseC2Ev:
Leh_func_begin3:
	pushq	%rbp
Ltmp4:
	movq	%rsp, %rbp
Ltmp5:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	__ZTV4Base@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	addq	%rdx, %rcx
	movq	%rcx, (%rax)
	movq	-8(%rbp), %rax
	movl	$0, 8(%rax)
	movq	-8(%rbp), %rax
	movl	$0, 12(%rax)
	popq	%rbp
	ret
Leh_func_end3:

	.globl	__ZN10SecondBaseC2Ev
.weak_definition __ZN10SecondBaseC2Ev
	.align	1, 0x90
__ZN10SecondBaseC2Ev:
Leh_func_begin4:
	pushq	%rbp
Ltmp6:
	movq	%rsp, %rbp
Ltmp7:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	__ZTV10SecondBase@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	addq	%rdx, %rcx
	movq	%rcx, (%rax)
	movq	-8(%rbp), %rax
	movl	$0, 8(%rax)
	movq	-8(%rbp), %rax
	movl	$1, 12(%rax)
	popq	%rbp
	ret
Leh_func_end4:

	.globl	__ZN7PlusOneC2Ev
.weak_definition __ZN7PlusOneC2Ev
	.align	1, 0x90
__ZN7PlusOneC2Ev:
Leh_func_begin5:
	pushq	%rbp
Ltmp8:
	movq	%rsp, %rbp
Ltmp9:
	subq	$16, %rsp
Ltmp10:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	callq	__ZN4BaseC2Ev
	movq	-8(%rbp), %rax
	movq	__ZTV7PlusOne@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	addq	%rdx, %rcx
	movq	%rcx, (%rax)
	movq	-8(%rbp), %rax
	movl	$2, 16(%rax)
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end5:

	.globl	__ZN7PlusOne3setEi
.weak_definition __ZN7PlusOne3setEi
	.align	1, 0x90
__ZN7PlusOne3setEi:
Leh_func_begin6:
	pushq	%rbp
Ltmp11:
	movq	%rsp, %rbp
Ltmp12:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	-12(%rbp), %eax
	addl	$1, %eax
	movq	-8(%rbp), %rcx
	movl	%eax, 8(%rcx)
	popq	%rbp
	ret
Leh_func_end6:

	.globl	__ZN7PlusOneC1Ev
.weak_definition __ZN7PlusOneC1Ev
	.align	1, 0x90
__ZN7PlusOneC1Ev:
Leh_func_begin7:
	pushq	%rbp
Ltmp13:
	movq	%rsp, %rbp
Ltmp14:
	subq	$16, %rsp
Ltmp15:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	callq	__ZN4BaseC2Ev
	movq	-8(%rbp), %rax
	movq	__ZTV7PlusOne@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	addq	%rdx, %rcx
	movq	%rcx, (%rax)
	movq	-8(%rbp), %rax
	movl	$2, 16(%rax)
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end7:

	.globl	__ZN8MinusOneC1Ev
.weak_definition __ZN8MinusOneC1Ev
	.align	1, 0x90
__ZN8MinusOneC1Ev:
Leh_func_begin8:
	pushq	%rbp
Ltmp16:
	movq	%rsp, %rbp
Ltmp17:
	subq	$16, %rsp
Ltmp18:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	callq	__ZN4BaseC2Ev
	movq	-8(%rbp), %rax
	movq	__ZTV8MinusOne@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	addq	%rdx, %rcx
	movq	%rcx, (%rax)
	movq	-8(%rbp), %rax
	movl	$3, 16(%rax)
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end8:

	.globl	__ZN8MinusOne3setEi
.weak_definition __ZN8MinusOne3setEi
	.align	1, 0x90
__ZN8MinusOne3setEi:
Leh_func_begin9:
	pushq	%rbp
Ltmp19:
	movq	%rsp, %rbp
Ltmp20:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	-12(%rbp), %eax
	subl	$1, %eax
	movq	-8(%rbp), %rcx
	movl	%eax, 8(%rcx)
	popq	%rbp
	ret
Leh_func_end9:

	.globl	__ZN7PlusTwoC1Ev
.weak_definition __ZN7PlusTwoC1Ev
	.align	1, 0x90
__ZN7PlusTwoC1Ev:
Leh_func_begin10:
	pushq	%rbp
Ltmp21:
	movq	%rsp, %rbp
Ltmp22:
	subq	$16, %rsp
Ltmp23:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	callq	__ZN7PlusOneC2Ev
	movq	-8(%rbp), %rax
	movabsq	$24, %rcx
	addq	%rcx, %rax
	movq	%rax, %rdi
	callq	__ZN10SecondBaseC2Ev
	movq	-8(%rbp), %rax
	movq	__ZTV7PlusTwo@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	movq	%rcx, %rsi
	addq	%rdx, %rsi
	movq	%rsi, (%rax)
	movq	-8(%rbp), %rax
	movabsq	$48, %rdx
	addq	%rdx, %rcx
	movq	%rcx, 24(%rax)
	movq	-8(%rbp), %rax
	movl	$4, 40(%rax)
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end10:

	.globl	__ZN7PlusTwo3setEi
.weak_definition __ZN7PlusTwo3setEi
	.align	1, 0x90
__ZN7PlusTwo3setEi:
Leh_func_begin11:
	pushq	%rbp
Ltmp24:
	movq	%rsp, %rbp
Ltmp25:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	-12(%rbp), %eax
	addl	$2, %eax
	movq	-8(%rbp), %rcx
	movl	%eax, 8(%rcx)
	popq	%rbp
	ret
Leh_func_end11:

	.globl	__ZN7PlusTwo4set2Ei
.weak_definition __ZN7PlusTwo4set2Ei
	.align	1, 0x90
__ZN7PlusTwo4set2Ei:
Leh_func_begin12:
	pushq	%rbp
Ltmp26:
	movq	%rsp, %rbp
Ltmp27:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	-12(%rbp), %eax
	addl	$2, %eax
	movq	-8(%rbp), %rcx
	movl	%eax, 32(%rcx)
	popq	%rbp
	ret
Leh_func_end12:

	.globl	__ZThn24_N7PlusTwo4set2Ei
.weak_definition __ZThn24_N7PlusTwo4set2Ei
	.align	4, 0x90
__ZThn24_N7PlusTwo4set2Ei:
Leh_func_begin13:
	pushq	%rbp
Ltmp28:
	movq	%rsp, %rbp
Ltmp29:
	subq	$16, %rsp
Ltmp30:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movq	-8(%rbp), %rax
	movabsq	$-24, %rcx
	addq	%rcx, %rax
	movl	-12(%rbp), %ecx
	movq	%rax, %rdi
	movl	%ecx, %esi
	callq	__ZN7PlusTwo4set2Ei
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end13:

	.section	__TEXT,__StaticInit,regular,pure_instructions
	.align	4, 0x90
__Z41__static_initialization_and_destruction_0ii:
Leh_func_begin14:
	pushq	%rbp
Ltmp31:
	movq	%rsp, %rbp
Ltmp32:
	subq	$16, %rsp
Ltmp33:
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-4(%rbp), %eax
	cmpl	$1, %eax
	jne	LBB14_3
	movl	-8(%rbp), %eax
	cmpl	$65535, %eax
	jne	LBB14_3
	leaq	__ZStL8__ioinit(%rip), %rax
	movq	%rax, %rdi
	callq	__ZNSt8ios_base4InitC1Ev
	leaq	___tcf_0(%rip), %rax
	movabsq	$0, %rcx
	movq	___dso_handle@GOTPCREL(%rip), %rdx
	leaq	(%rdx), %rdx
	movq	%rax, %rdi
	movq	%rcx, %rsi
	callq	___cxa_atexit
LBB14_3:
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end14:

	.section	__TEXT,__text,regular,pure_instructions
	.align	4, 0x90
___tcf_0:
Leh_func_begin15:
	pushq	%rbp
Ltmp34:
	movq	%rsp, %rbp
Ltmp35:
	subq	$16, %rsp
Ltmp36:
	movq	%rdi, -8(%rbp)
	leaq	__ZStL8__ioinit(%rip), %rax
	movq	%rax, %rdi
	callq	__ZNSt8ios_base4InitD1Ev
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end15:

	.globl	__Z18store_and_retrieveiP4Base
	.align	4, 0x90
__Z18store_and_retrieveiP4Base:
Leh_func_begin16:
	pushq	%rbp
Ltmp37:
	movq	%rsp, %rbp
Ltmp38:
	subq	$32, %rsp
Ltmp39:
	movl	%edi, -4(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-16(%rbp), %rax
	cmpq	$0, %rax
	je	LBB16_2
	movq	-16(%rbp), %rax
	movq	(%rax), %rax
	movq	-8(%rax), %rax
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	callq	__ZNKSt9type_info4nameEv
	jmp	LBB16_3
LBB16_2:
	callq	___cxa_bad_typeid
LBB16_3:
	addq	$32, %rsp
	popq	%rbp
	ret
Leh_func_end16:

	.globl	_main
	.align	4, 0x90
_main:
Leh_func_begin17:
	pushq	%rbp
Ltmp40:
	movq	%rsp, %rbp
Ltmp41:
	subq	$64, %rsp
Ltmp42:
	movabsq	$24, %rax
	movq	%rax, %rdi
	movq	%rax, -48(%rbp)
	callq	__Znwm
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rax
	movq	%rax, %rdi
	callq	__ZN7PlusOneC1Ev
	movq	-32(%rbp), %rax
	movq	%rax, -40(%rbp)
	movq	-40(%rbp), %rax
	movl	$10, %ecx
	movl	%ecx, %edi
	movq	%rax, %rsi
	movl	%ecx, -52(%rbp)
	callq	__Z18store_and_retrieveiP4Base
	movq	-48(%rbp), %rdi
	callq	__Znwm
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	callq	__ZN8MinusOneC1Ev
	movq	-24(%rbp), %rax
	movq	%rax, -40(%rbp)
	movq	-40(%rbp), %rax
	movl	-52(%rbp), %ecx
	movl	%ecx, %edi
	movq	%rax, %rsi
	callq	__Z18store_and_retrieveiP4Base
	movabsq	$48, %rax
	movq	%rax, %rdi
	callq	__Znwm
	movq	%rax, -16(%rbp)
	movq	-16(%rbp), %rax
	movq	%rax, %rdi
	callq	__ZN7PlusTwoC1Ev
	movq	-16(%rbp), %rax
	movq	%rax, -40(%rbp)
	movq	-40(%rbp), %rax
	movl	-52(%rbp), %ecx
	movl	%ecx, %edi
	movq	%rax, %rsi
	callq	__Z18store_and_retrieveiP4Base
	movl	$0, -8(%rbp)
	movl	-8(%rbp), %eax
	movl	%eax, -4(%rbp)
	movl	-4(%rbp), %eax
	addq	$64, %rsp
	popq	%rbp
	ret
Leh_func_end17:

	.section	__DATA,__data
	.globl	___classnames
	.align	5
___classnames:
	.quad	L_.str
	.quad	L_.str1
	.quad	L_.str2
	.quad	L_.str3
	.quad	L_.str4

	.section	__DATA,__datacoal_nt,coalesced
	.globl	__ZTV4Base
.weak_definition __ZTV4Base
	.align	4
__ZTV4Base:
	.quad	0
	.quad	__ZTI4Base
	.quad	___cxa_pure_virtual

	.globl	__ZTI4Base
.weak_definition __ZTI4Base
	.align	4
__ZTI4Base:
	.quad	__ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	__ZTS4Base

	.section	__TEXT,__const_coal,coalesced,pure_instructions
	.globl	__ZTS4Base
.weak_definition __ZTS4Base
__ZTS4Base:
	.asciz	 "4Base"

	.section	__DATA,__datacoal_nt,coalesced
	.globl	__ZTV10SecondBase
.weak_definition __ZTV10SecondBase
	.align	4
__ZTV10SecondBase:
	.quad	0
	.quad	__ZTI10SecondBase
	.quad	___cxa_pure_virtual

	.globl	__ZTI10SecondBase
.weak_definition __ZTI10SecondBase
	.align	4
__ZTI10SecondBase:
	.quad	__ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	__ZTS10SecondBase

	.section	__TEXT,__const_coal,coalesced,pure_instructions
	.globl	__ZTS10SecondBase
.weak_definition __ZTS10SecondBase
__ZTS10SecondBase:
	.asciz	 "10SecondBase"

	.section	__DATA,__datacoal_nt,coalesced
	.globl	__ZTV7PlusOne
.weak_definition __ZTV7PlusOne
	.align	4
__ZTV7PlusOne:
	.quad	0
	.quad	__ZTI7PlusOne
	.quad	__ZN7PlusOne3setEi

	.globl	__ZTI7PlusOne
.weak_definition __ZTI7PlusOne
	.align	4
__ZTI7PlusOne:
	.quad	__ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	__ZTS7PlusOne
	.quad	__ZTI4Base

	.section	__TEXT,__const_coal,coalesced,pure_instructions
	.globl	__ZTS7PlusOne
.weak_definition __ZTS7PlusOne
__ZTS7PlusOne:
	.asciz	 "7PlusOne"

	.section	__DATA,__datacoal_nt,coalesced
	.globl	__ZTV8MinusOne
.weak_definition __ZTV8MinusOne
	.align	4
__ZTV8MinusOne:
	.quad	0
	.quad	__ZTI8MinusOne
	.quad	__ZN8MinusOne3setEi

	.globl	__ZTI8MinusOne
.weak_definition __ZTI8MinusOne
	.align	4
__ZTI8MinusOne:
	.quad	__ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	__ZTS8MinusOne
	.quad	__ZTI4Base

	.section	__TEXT,__const_coal,coalesced,pure_instructions
	.globl	__ZTS8MinusOne
.weak_definition __ZTS8MinusOne
__ZTS8MinusOne:
	.asciz	 "8MinusOne"

	.section	__DATA,__datacoal_nt,coalesced
	.globl	__ZTV7PlusTwo
.weak_definition __ZTV7PlusTwo
	.align	5
__ZTV7PlusTwo:
	.quad	0
	.quad	__ZTI7PlusTwo
	.quad	__ZN7PlusTwo3setEi
	.quad	__ZN7PlusTwo4set2Ei
	.quad	-24
	.quad	__ZTI7PlusTwo
	.quad	__ZThn24_N7PlusTwo4set2Ei

	.globl	__ZTI7PlusTwo
.weak_definition __ZTI7PlusTwo
	.align	5
__ZTI7PlusTwo:
	.quad	__ZTVN10__cxxabiv121__vmi_class_type_infoE+16
	.quad	__ZTS7PlusTwo
	.long	0
	.long	2
	.quad	__ZTI7PlusOne
	.quad	2
	.quad	__ZTI10SecondBase
	.quad	6146

	.section	__TEXT,__const_coal,coalesced,pure_instructions
	.globl	__ZTS7PlusTwo
.weak_definition __ZTS7PlusTwo
__ZTS7PlusTwo:
	.asciz	 "7PlusTwo"

.zerofill __DATA,__bss,__ZStL8__ioinit,1,3
	.section	__TEXT,__cstring,cstring_literals
L_.str:
	.asciz	 "Base"

L_.str1:
	.asciz	 "SecondBase"

L_.str2:
	.asciz	 "PlusOne"

L_.str3:
	.asciz	 "MinusOne"

L_.str4:
	.asciz	 "PlusTwo"

	.section	__DATA,__mod_init_func,mod_init_funcs
	.align	3
	.quad	__GLOBAL__I___classnames
	.section	__TEXT,__eh_frame,coalesced,no_toc+strip_static_syms+live_support
EH_frame0:
Lsection_eh_frame:
Leh_frame_common:
Lset0 = Leh_frame_common_end-Leh_frame_common_begin
	.long	Lset0
Leh_frame_common_begin:
	.long	0
	.byte	1
	.asciz	 "zR"
	.byte	1
	.byte	120
	.byte	16
	.byte	1
	.byte	16
	.byte	12
	.byte	7
	.byte	8
	.byte	144
	.byte	1
	.align	3
Leh_frame_common_end:
__GLOBAL__I___classnames.eh:
Lset1 = Leh_frame_end1-Leh_frame_begin1
	.long	Lset1
Leh_frame_begin1:
Lset2 = Leh_frame_begin1-Leh_frame_common
	.long	Lset2
Ltmp43:
	.quad	Leh_func_begin1-Ltmp43
Lset3 = Leh_func_end1-Leh_func_begin1
	.quad	Lset3
	.byte	0
	.byte	4
Lset4 = Ltmp0-Leh_func_begin1
	.long	Lset4
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset5 = Ltmp1-Ltmp0
	.long	Lset5
	.byte	13
	.byte	6
	.align	3
Leh_frame_end1:

	.globl	__ZNKSt9type_info4nameEv.eh
.weak_definition __ZNKSt9type_info4nameEv.eh
__ZNKSt9type_info4nameEv.eh:
Lset6 = Leh_frame_end2-Leh_frame_begin2
	.long	Lset6
Leh_frame_begin2:
Lset7 = Leh_frame_begin2-Leh_frame_common
	.long	Lset7
Ltmp44:
	.quad	Leh_func_begin2-Ltmp44
Lset8 = Leh_func_end2-Leh_func_begin2
	.quad	Lset8
	.byte	0
	.byte	4
Lset9 = Ltmp2-Leh_func_begin2
	.long	Lset9
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset10 = Ltmp3-Ltmp2
	.long	Lset10
	.byte	13
	.byte	6
	.align	3
Leh_frame_end2:

	.globl	__ZN4BaseC2Ev.eh
.weak_definition __ZN4BaseC2Ev.eh
__ZN4BaseC2Ev.eh:
Lset11 = Leh_frame_end3-Leh_frame_begin3
	.long	Lset11
Leh_frame_begin3:
Lset12 = Leh_frame_begin3-Leh_frame_common
	.long	Lset12
Ltmp45:
	.quad	Leh_func_begin3-Ltmp45
Lset13 = Leh_func_end3-Leh_func_begin3
	.quad	Lset13
	.byte	0
	.byte	4
Lset14 = Ltmp4-Leh_func_begin3
	.long	Lset14
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset15 = Ltmp5-Ltmp4
	.long	Lset15
	.byte	13
	.byte	6
	.align	3
Leh_frame_end3:

	.globl	__ZN10SecondBaseC2Ev.eh
.weak_definition __ZN10SecondBaseC2Ev.eh
__ZN10SecondBaseC2Ev.eh:
Lset16 = Leh_frame_end4-Leh_frame_begin4
	.long	Lset16
Leh_frame_begin4:
Lset17 = Leh_frame_begin4-Leh_frame_common
	.long	Lset17
Ltmp46:
	.quad	Leh_func_begin4-Ltmp46
Lset18 = Leh_func_end4-Leh_func_begin4
	.quad	Lset18
	.byte	0
	.byte	4
Lset19 = Ltmp6-Leh_func_begin4
	.long	Lset19
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset20 = Ltmp7-Ltmp6
	.long	Lset20
	.byte	13
	.byte	6
	.align	3
Leh_frame_end4:

	.globl	__ZN7PlusOneC2Ev.eh
.weak_definition __ZN7PlusOneC2Ev.eh
__ZN7PlusOneC2Ev.eh:
Lset21 = Leh_frame_end5-Leh_frame_begin5
	.long	Lset21
Leh_frame_begin5:
Lset22 = Leh_frame_begin5-Leh_frame_common
	.long	Lset22
Ltmp47:
	.quad	Leh_func_begin5-Ltmp47
Lset23 = Leh_func_end5-Leh_func_begin5
	.quad	Lset23
	.byte	0
	.byte	4
Lset24 = Ltmp8-Leh_func_begin5
	.long	Lset24
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset25 = Ltmp9-Ltmp8
	.long	Lset25
	.byte	13
	.byte	6
	.align	3
Leh_frame_end5:

	.globl	__ZN7PlusOne3setEi.eh
.weak_definition __ZN7PlusOne3setEi.eh
__ZN7PlusOne3setEi.eh:
Lset26 = Leh_frame_end6-Leh_frame_begin6
	.long	Lset26
Leh_frame_begin6:
Lset27 = Leh_frame_begin6-Leh_frame_common
	.long	Lset27
Ltmp48:
	.quad	Leh_func_begin6-Ltmp48
Lset28 = Leh_func_end6-Leh_func_begin6
	.quad	Lset28
	.byte	0
	.byte	4
Lset29 = Ltmp11-Leh_func_begin6
	.long	Lset29
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset30 = Ltmp12-Ltmp11
	.long	Lset30
	.byte	13
	.byte	6
	.align	3
Leh_frame_end6:

	.globl	__ZN7PlusOneC1Ev.eh
.weak_definition __ZN7PlusOneC1Ev.eh
__ZN7PlusOneC1Ev.eh:
Lset31 = Leh_frame_end7-Leh_frame_begin7
	.long	Lset31
Leh_frame_begin7:
Lset32 = Leh_frame_begin7-Leh_frame_common
	.long	Lset32
Ltmp49:
	.quad	Leh_func_begin7-Ltmp49
Lset33 = Leh_func_end7-Leh_func_begin7
	.quad	Lset33
	.byte	0
	.byte	4
Lset34 = Ltmp13-Leh_func_begin7
	.long	Lset34
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset35 = Ltmp14-Ltmp13
	.long	Lset35
	.byte	13
	.byte	6
	.align	3
Leh_frame_end7:

	.globl	__ZN8MinusOneC1Ev.eh
.weak_definition __ZN8MinusOneC1Ev.eh
__ZN8MinusOneC1Ev.eh:
Lset36 = Leh_frame_end8-Leh_frame_begin8
	.long	Lset36
Leh_frame_begin8:
Lset37 = Leh_frame_begin8-Leh_frame_common
	.long	Lset37
Ltmp50:
	.quad	Leh_func_begin8-Ltmp50
Lset38 = Leh_func_end8-Leh_func_begin8
	.quad	Lset38
	.byte	0
	.byte	4
Lset39 = Ltmp16-Leh_func_begin8
	.long	Lset39
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset40 = Ltmp17-Ltmp16
	.long	Lset40
	.byte	13
	.byte	6
	.align	3
Leh_frame_end8:

	.globl	__ZN8MinusOne3setEi.eh
.weak_definition __ZN8MinusOne3setEi.eh
__ZN8MinusOne3setEi.eh:
Lset41 = Leh_frame_end9-Leh_frame_begin9
	.long	Lset41
Leh_frame_begin9:
Lset42 = Leh_frame_begin9-Leh_frame_common
	.long	Lset42
Ltmp51:
	.quad	Leh_func_begin9-Ltmp51
Lset43 = Leh_func_end9-Leh_func_begin9
	.quad	Lset43
	.byte	0
	.byte	4
Lset44 = Ltmp19-Leh_func_begin9
	.long	Lset44
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset45 = Ltmp20-Ltmp19
	.long	Lset45
	.byte	13
	.byte	6
	.align	3
Leh_frame_end9:

	.globl	__ZN7PlusTwoC1Ev.eh
.weak_definition __ZN7PlusTwoC1Ev.eh
__ZN7PlusTwoC1Ev.eh:
Lset46 = Leh_frame_end10-Leh_frame_begin10
	.long	Lset46
Leh_frame_begin10:
Lset47 = Leh_frame_begin10-Leh_frame_common
	.long	Lset47
Ltmp52:
	.quad	Leh_func_begin10-Ltmp52
Lset48 = Leh_func_end10-Leh_func_begin10
	.quad	Lset48
	.byte	0
	.byte	4
Lset49 = Ltmp21-Leh_func_begin10
	.long	Lset49
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset50 = Ltmp22-Ltmp21
	.long	Lset50
	.byte	13
	.byte	6
	.align	3
Leh_frame_end10:

	.globl	__ZN7PlusTwo3setEi.eh
.weak_definition __ZN7PlusTwo3setEi.eh
__ZN7PlusTwo3setEi.eh:
Lset51 = Leh_frame_end11-Leh_frame_begin11
	.long	Lset51
Leh_frame_begin11:
Lset52 = Leh_frame_begin11-Leh_frame_common
	.long	Lset52
Ltmp53:
	.quad	Leh_func_begin11-Ltmp53
Lset53 = Leh_func_end11-Leh_func_begin11
	.quad	Lset53
	.byte	0
	.byte	4
Lset54 = Ltmp24-Leh_func_begin11
	.long	Lset54
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset55 = Ltmp25-Ltmp24
	.long	Lset55
	.byte	13
	.byte	6
	.align	3
Leh_frame_end11:

	.globl	__ZN7PlusTwo4set2Ei.eh
.weak_definition __ZN7PlusTwo4set2Ei.eh
__ZN7PlusTwo4set2Ei.eh:
Lset56 = Leh_frame_end12-Leh_frame_begin12
	.long	Lset56
Leh_frame_begin12:
Lset57 = Leh_frame_begin12-Leh_frame_common
	.long	Lset57
Ltmp54:
	.quad	Leh_func_begin12-Ltmp54
Lset58 = Leh_func_end12-Leh_func_begin12
	.quad	Lset58
	.byte	0
	.byte	4
Lset59 = Ltmp26-Leh_func_begin12
	.long	Lset59
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset60 = Ltmp27-Ltmp26
	.long	Lset60
	.byte	13
	.byte	6
	.align	3
Leh_frame_end12:

	.globl	__ZThn24_N7PlusTwo4set2Ei.eh
.weak_definition __ZThn24_N7PlusTwo4set2Ei.eh
__ZThn24_N7PlusTwo4set2Ei.eh:
Lset61 = Leh_frame_end13-Leh_frame_begin13
	.long	Lset61
Leh_frame_begin13:
Lset62 = Leh_frame_begin13-Leh_frame_common
	.long	Lset62
Ltmp55:
	.quad	Leh_func_begin13-Ltmp55
Lset63 = Leh_func_end13-Leh_func_begin13
	.quad	Lset63
	.byte	0
	.byte	4
Lset64 = Ltmp28-Leh_func_begin13
	.long	Lset64
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset65 = Ltmp29-Ltmp28
	.long	Lset65
	.byte	13
	.byte	6
	.align	3
Leh_frame_end13:

__Z41__static_initialization_and_destruction_0ii.eh:
Lset66 = Leh_frame_end14-Leh_frame_begin14
	.long	Lset66
Leh_frame_begin14:
Lset67 = Leh_frame_begin14-Leh_frame_common
	.long	Lset67
Ltmp56:
	.quad	Leh_func_begin14-Ltmp56
Lset68 = Leh_func_end14-Leh_func_begin14
	.quad	Lset68
	.byte	0
	.byte	4
Lset69 = Ltmp31-Leh_func_begin14
	.long	Lset69
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset70 = Ltmp32-Ltmp31
	.long	Lset70
	.byte	13
	.byte	6
	.align	3
Leh_frame_end14:

___tcf_0.eh:
Lset71 = Leh_frame_end15-Leh_frame_begin15
	.long	Lset71
Leh_frame_begin15:
Lset72 = Leh_frame_begin15-Leh_frame_common
	.long	Lset72
Ltmp57:
	.quad	Leh_func_begin15-Ltmp57
Lset73 = Leh_func_end15-Leh_func_begin15
	.quad	Lset73
	.byte	0
	.byte	4
Lset74 = Ltmp34-Leh_func_begin15
	.long	Lset74
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset75 = Ltmp35-Ltmp34
	.long	Lset75
	.byte	13
	.byte	6
	.align	3
Leh_frame_end15:

	.globl	__Z18store_and_retrieveiP4Base.eh
__Z18store_and_retrieveiP4Base.eh:
Lset76 = Leh_frame_end16-Leh_frame_begin16
	.long	Lset76
Leh_frame_begin16:
Lset77 = Leh_frame_begin16-Leh_frame_common
	.long	Lset77
Ltmp58:
	.quad	Leh_func_begin16-Ltmp58
Lset78 = Leh_func_end16-Leh_func_begin16
	.quad	Lset78
	.byte	0
	.byte	4
Lset79 = Ltmp37-Leh_func_begin16
	.long	Lset79
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset80 = Ltmp38-Ltmp37
	.long	Lset80
	.byte	13
	.byte	6
	.align	3
Leh_frame_end16:

	.globl	_main.eh
_main.eh:
Lset81 = Leh_frame_end17-Leh_frame_begin17
	.long	Lset81
Leh_frame_begin17:
Lset82 = Leh_frame_begin17-Leh_frame_common
	.long	Lset82
Ltmp59:
	.quad	Leh_func_begin17-Ltmp59
Lset83 = Leh_func_end17-Leh_func_begin17
	.quad	Lset83
	.byte	0
	.byte	4
Lset84 = Ltmp40-Leh_func_begin17
	.long	Lset84
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset85 = Ltmp41-Ltmp40
	.long	Lset85
	.byte	13
	.byte	6
	.align	3
Leh_frame_end17:


.subsections_via_symbols
