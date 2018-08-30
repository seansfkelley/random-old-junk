	.section	__TEXT,__text,regular,pure_instructions
	.globl	store_and_retrieve(int, Base*)
	.align	4, 0x90
store_and_retrieve(int, Base*):
Leh_func_begin1:
	pushq	%rbp
Ltmp0:
	movq	%rsp, %rbp
Ltmp1:
	subq	$32, %rsp
Ltmp2:
	movl	%edi, -4(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-16(%rbp), %rax
	cmpq	$0, %rax
	je	LBB1_2
	movq	-16(%rbp), %rax
	movq	(%rax), %rax
	movq	-8(%rax), %rax
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	callq	std::type_info::name() const
	jmp	LBB1_3
LBB1_2:
	callq	___cxa_bad_typeid
LBB1_3:
	addq	$32, %rsp
	popq	%rbp
	ret
Leh_func_end1:

	.section	__TEXT,__StaticInit,regular,pure_instructions
	.align	4, 0x90
global constructors keyed to _Z18store_and_retrieveiP4Base:
Leh_func_begin2:
	pushq	%rbp
Ltmp3:
	movq	%rsp, %rbp
Ltmp4:
	movl	$1, %eax
	movl	$65535, %ecx
	movl	%eax, %edi
	movl	%ecx, %esi
	callq	__static_initialization_and_destruction_0(int, int)
	popq	%rbp
	ret
Leh_func_end2:

	.section	__TEXT,__textcoal_nt,coalesced,pure_instructions
	.globl	std::type_info::name() const
.weak_definition std::type_info::name() const
	.align	1, 0x90
std::type_info::name() const:
Leh_func_begin3:
	pushq	%rbp
Ltmp5:
	movq	%rsp, %rbp
Ltmp6:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, -16(%rbp)
	movq	-16(%rbp), %rax
	popq	%rbp
	ret
Leh_func_end3:

	.globl	Base::Base()
.weak_definition Base::Base()
	.align	1, 0x90
Base::Base():
Leh_func_begin4:
	pushq	%rbp
Ltmp7:
	movq	%rsp, %rbp
Ltmp8:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	vtable for Base@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	addq	%rdx, %rcx
	movq	%rcx, (%rax)
	movq	-8(%rbp), %rax
	movl	$0, 8(%rax)
	popq	%rbp
	ret
Leh_func_end4:

	.globl	PlusOne::set(int)
.weak_definition PlusOne::set(int)
	.align	1, 0x90
PlusOne::set(int):
Leh_func_begin5:
	pushq	%rbp
Ltmp9:
	movq	%rsp, %rbp
Ltmp10:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	-12(%rbp), %eax
	addl	$1, %eax
	movq	-8(%rbp), %rcx
	movl	%eax, 8(%rcx)
	popq	%rbp
	ret
Leh_func_end5:

	.globl	MinusOne::set(int)
.weak_definition MinusOne::set(int)
	.align	1, 0x90
MinusOne::set(int):
Leh_func_begin6:
	pushq	%rbp
Ltmp11:
	movq	%rsp, %rbp
Ltmp12:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	-12(%rbp), %eax
	subl	$1, %eax
	movq	-8(%rbp), %rcx
	movl	%eax, 8(%rcx)
	popq	%rbp
	ret
Leh_func_end6:

	.globl	PlusOne::PlusOne()
.weak_definition PlusOne::PlusOne()
	.align	1, 0x90
PlusOne::PlusOne():
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
	callq	Base::Base()
	movq	-8(%rbp), %rax
	movq	vtable for PlusOne@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	addq	%rdx, %rcx
	movq	%rcx, (%rax)
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end7:

	.globl	MinusOne::MinusOne()
.weak_definition MinusOne::MinusOne()
	.align	1, 0x90
MinusOne::MinusOne():
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
	callq	Base::Base()
	movq	-8(%rbp), %rax
	movq	vtable for MinusOne@GOTPCREL(%rip), %rcx
	leaq	(%rcx), %rcx
	movabsq	$16, %rdx
	addq	%rdx, %rcx
	movq	%rcx, (%rax)
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end8:

	.section	__TEXT,__StaticInit,regular,pure_instructions
	.align	4, 0x90
__static_initialization_and_destruction_0(int, int):
Leh_func_begin9:
	pushq	%rbp
Ltmp19:
	movq	%rsp, %rbp
Ltmp20:
	subq	$16, %rsp
Ltmp21:
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-4(%rbp), %eax
	cmpl	$1, %eax
	jne	LBB9_3
	movl	-8(%rbp), %eax
	cmpl	$65535, %eax
	jne	LBB9_3
	leaq	std::__ioinit(%rip), %rax
	movq	%rax, %rdi
	callq	std::ios_base::Init::Init()
	leaq	___tcf_0(%rip), %rax
	movabsq	$0, %rcx
	movq	___dso_handle@GOTPCREL(%rip), %rdx
	leaq	(%rdx), %rdx
	movq	%rax, %rdi
	movq	%rcx, %rsi
	callq	___cxa_atexit
LBB9_3:
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end9:

	.section	__TEXT,__text,regular,pure_instructions
	.align	4, 0x90
___tcf_0:
Leh_func_begin10:
	pushq	%rbp
Ltmp22:
	movq	%rsp, %rbp
Ltmp23:
	subq	$16, %rsp
Ltmp24:
	movq	%rdi, -8(%rbp)
	leaq	std::__ioinit(%rip), %rax
	movq	%rax, %rdi
	callq	std::ios_base::Init::~Init()
	addq	$16, %rsp
	popq	%rbp
	ret
Leh_func_end10:

	.globl	_main
	.align	4, 0x90
_main:
Leh_func_begin11:
	pushq	%rbp
Ltmp25:
	movq	%rsp, %rbp
Ltmp26:
	subq	$48, %rsp
Ltmp27:
	movabsq	$16, %rax
	movq	%rax, %rdi
	movq	%rax, -40(%rbp)
	callq	operator new(unsigned long)
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	callq	PlusOne::PlusOne()
	movq	-24(%rbp), %rax
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rax
	movl	$10, %ecx
	movl	%ecx, %edi
	movq	%rax, %rsi
	movl	%ecx, -44(%rbp)
	callq	store_and_retrieve(int, Base*)
	movq	-40(%rbp), %rdi
	callq	operator new(unsigned long)
	movq	%rax, -16(%rbp)
	movq	-16(%rbp), %rax
	movq	%rax, %rdi
	callq	MinusOne::MinusOne()
	movq	-16(%rbp), %rax
	movq	%rax, -32(%rbp)
	movq	-32(%rbp), %rax
	movl	-44(%rbp), %ecx
	movl	%ecx, %edi
	movq	%rax, %rsi
	callq	store_and_retrieve(int, Base*)
	movl	$0, -8(%rbp)
	movl	-8(%rbp), %eax
	movl	%eax, -4(%rbp)
	movl	-4(%rbp), %eax
	addq	$48, %rsp
	popq	%rbp
	ret
Leh_func_end11:

	.section	__DATA,__datacoal_nt,coalesced
	.globl	vtable for Base
.weak_definition vtable for Base
	.align	4
vtable for Base:
	.quad	0
	.quad	typeinfo for Base
	.quad	___cxa_pure_virtual

	.globl	typeinfo for Base
.weak_definition typeinfo for Base
	.align	4
typeinfo for Base:
	.quad	vtable for __cxxabiv1::__class_type_info+16
	.quad	typeinfo name for Base

	.section	__TEXT,__const_coal,coalesced,pure_instructions
	.globl	typeinfo name for Base
.weak_definition typeinfo name for Base
typeinfo name for Base:
	.asciz	 "Base"

	.section	__DATA,__datacoal_nt,coalesced
	.globl	vtable for PlusOne
.weak_definition vtable for PlusOne
	.align	4
vtable for PlusOne:
	.quad	0
	.quad	typeinfo for PlusOne
	.quad	PlusOne::set(int)

	.globl	typeinfo for PlusOne
.weak_definition typeinfo for PlusOne
	.align	4
typeinfo for PlusOne:
	.quad	vtable for __cxxabiv1::__si_class_type_info+16
	.quad	typeinfo name for PlusOne
	.quad	typeinfo for Base

	.section	__TEXT,__const_coal,coalesced,pure_instructions
	.globl	typeinfo name for PlusOne
.weak_definition typeinfo name for PlusOne
typeinfo name for PlusOne:
	.asciz	 "PlusOne"

	.section	__DATA,__datacoal_nt,coalesced
	.globl	vtable for MinusOne
.weak_definition vtable for MinusOne
	.align	4
vtable for MinusOne:
	.quad	0
	.quad	typeinfo for MinusOne
	.quad	MinusOne::set(int)

	.globl	typeinfo for MinusOne
.weak_definition typeinfo for MinusOne
	.align	4
typeinfo for MinusOne:
	.quad	vtable for __cxxabiv1::__si_class_type_info+16
	.quad	typeinfo name for MinusOne
	.quad	typeinfo for Base

	.section	__TEXT,__const_coal,coalesced,pure_instructions
	.globl	typeinfo name for MinusOne
.weak_definition typeinfo name for MinusOne
typeinfo name for MinusOne:
	.asciz	 "MinusOne"

.zerofill __DATA,__bss,std::__ioinit,1,3
	.section	__DATA,__mod_init_func,mod_init_funcs
	.align	3
	.quad	global constructors keyed to _Z18store_and_retrieveiP4Base
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
	.globl	__Z18store_and_retrieveiP4Base.eh
__Z18store_and_retrieveiP4Base.eh:
Lset1 = Leh_frame_end1-Leh_frame_begin1
	.long	Lset1
Leh_frame_begin1:
Lset2 = Leh_frame_begin1-Leh_frame_common
	.long	Lset2
Ltmp28:
	.quad	Leh_func_begin1-Ltmp28
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

global constructors keyed to _Z18store_and_retrieveiP4Base.eh:
Lset6 = Leh_frame_end2-Leh_frame_begin2
	.long	Lset6
Leh_frame_begin2:
Lset7 = Leh_frame_begin2-Leh_frame_common
	.long	Lset7
Ltmp29:
	.quad	Leh_func_begin2-Ltmp29
Lset8 = Leh_func_end2-Leh_func_begin2
	.quad	Lset8
	.byte	0
	.byte	4
Lset9 = Ltmp3-Leh_func_begin2
	.long	Lset9
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset10 = Ltmp4-Ltmp3
	.long	Lset10
	.byte	13
	.byte	6
	.align	3
Leh_frame_end2:

	.globl	__ZNKSt9type_info4nameEv.eh
.weak_definition __ZNKSt9type_info4nameEv.eh
__ZNKSt9type_info4nameEv.eh:
Lset11 = Leh_frame_end3-Leh_frame_begin3
	.long	Lset11
Leh_frame_begin3:
Lset12 = Leh_frame_begin3-Leh_frame_common
	.long	Lset12
Ltmp30:
	.quad	Leh_func_begin3-Ltmp30
Lset13 = Leh_func_end3-Leh_func_begin3
	.quad	Lset13
	.byte	0
	.byte	4
Lset14 = Ltmp5-Leh_func_begin3
	.long	Lset14
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset15 = Ltmp6-Ltmp5
	.long	Lset15
	.byte	13
	.byte	6
	.align	3
Leh_frame_end3:

	.globl	__ZN4BaseC2Ev.eh
.weak_definition __ZN4BaseC2Ev.eh
__ZN4BaseC2Ev.eh:
Lset16 = Leh_frame_end4-Leh_frame_begin4
	.long	Lset16
Leh_frame_begin4:
Lset17 = Leh_frame_begin4-Leh_frame_common
	.long	Lset17
Ltmp31:
	.quad	Leh_func_begin4-Ltmp31
Lset18 = Leh_func_end4-Leh_func_begin4
	.quad	Lset18
	.byte	0
	.byte	4
Lset19 = Ltmp7-Leh_func_begin4
	.long	Lset19
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset20 = Ltmp8-Ltmp7
	.long	Lset20
	.byte	13
	.byte	6
	.align	3
Leh_frame_end4:

	.globl	__ZN7PlusOne3setEi.eh
.weak_definition __ZN7PlusOne3setEi.eh
__ZN7PlusOne3setEi.eh:
Lset21 = Leh_frame_end5-Leh_frame_begin5
	.long	Lset21
Leh_frame_begin5:
Lset22 = Leh_frame_begin5-Leh_frame_common
	.long	Lset22
Ltmp32:
	.quad	Leh_func_begin5-Ltmp32
Lset23 = Leh_func_end5-Leh_func_begin5
	.quad	Lset23
	.byte	0
	.byte	4
Lset24 = Ltmp9-Leh_func_begin5
	.long	Lset24
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset25 = Ltmp10-Ltmp9
	.long	Lset25
	.byte	13
	.byte	6
	.align	3
Leh_frame_end5:

	.globl	__ZN8MinusOne3setEi.eh
.weak_definition __ZN8MinusOne3setEi.eh
__ZN8MinusOne3setEi.eh:
Lset26 = Leh_frame_end6-Leh_frame_begin6
	.long	Lset26
Leh_frame_begin6:
Lset27 = Leh_frame_begin6-Leh_frame_common
	.long	Lset27
Ltmp33:
	.quad	Leh_func_begin6-Ltmp33
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
Ltmp34:
	.quad	Leh_func_begin7-Ltmp34
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
Ltmp35:
	.quad	Leh_func_begin8-Ltmp35
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

__Z41__static_initialization_and_destruction_0ii.eh:
Lset41 = Leh_frame_end9-Leh_frame_begin9
	.long	Lset41
Leh_frame_begin9:
Lset42 = Leh_frame_begin9-Leh_frame_common
	.long	Lset42
Ltmp36:
	.quad	Leh_func_begin9-Ltmp36
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

___tcf_0.eh:
Lset46 = Leh_frame_end10-Leh_frame_begin10
	.long	Lset46
Leh_frame_begin10:
Lset47 = Leh_frame_begin10-Leh_frame_common
	.long	Lset47
Ltmp37:
	.quad	Leh_func_begin10-Ltmp37
Lset48 = Leh_func_end10-Leh_func_begin10
	.quad	Lset48
	.byte	0
	.byte	4
Lset49 = Ltmp22-Leh_func_begin10
	.long	Lset49
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset50 = Ltmp23-Ltmp22
	.long	Lset50
	.byte	13
	.byte	6
	.align	3
Leh_frame_end10:

	.globl	_main.eh
_main.eh:
Lset51 = Leh_frame_end11-Leh_frame_begin11
	.long	Lset51
Leh_frame_begin11:
Lset52 = Leh_frame_begin11-Leh_frame_common
	.long	Lset52
Ltmp38:
	.quad	Leh_func_begin11-Ltmp38
Lset53 = Leh_func_end11-Leh_func_begin11
	.quad	Lset53
	.byte	0
	.byte	4
Lset54 = Ltmp25-Leh_func_begin11
	.long	Lset54
	.byte	14
	.byte	16
	.byte	134
	.byte	2
	.byte	4
Lset55 = Ltmp26-Ltmp25
	.long	Lset55
	.byte	13
	.byte	6
	.align	3
Leh_frame_end11:


.subsections_via_symbols
