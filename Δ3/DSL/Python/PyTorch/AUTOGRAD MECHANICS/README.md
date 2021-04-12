This note will present an overview of how autograd works and records the operations. It’s not strictly necessary to understand all this, but we recommend getting familiar with it, as it will help you write more efficient, cleaner programs, and can aid you in debugging.

Excluding subgraphs from backward
Every Tensor has a flag: requires_grad that allows for fine grained exclusion of subgraphs from gradient computation and can increase efficiency.

requires_grad
If there’s a single input to an operation that requires gradient, its output will also require gradient. Conversely, only if all inputs don’t require gradient, the output also won’t require it. Backward computation is never performed in the subgraphs, where all Tensors didn’t require gradients.

>>> x = torch.randn(5, 5)  # requires_grad=False by default
>>> y = torch.randn(5, 5)  # requires_grad=False by default
>>> z = torch.randn((5, 5), requires_grad=True)
>>> a = x + y
>>> a.requires_grad
False
>>> b = a + z
>>> b.requires_grad
True
This is especially useful when you want to freeze part of your model, or you know in advance that you’re not going to use gradients w.r.t. some parameters. For example if you want to finetune a pretrained CNN, it’s enough to switch the requires_grad flags in the frozen base, and no intermediate buffers will be saved, until the computation gets to the last layer, where the affine transform will use weights that require gradient, and the output of the network will also require them.

model = torchvision.models.resnet18(pretrained=True)
for param in model.parameters():
    param.requires_grad = False
# Replace the last fully-connected layer
# Parameters of newly constructed modules have requires_grad=True by default
model.fc = nn.Linear(512, 100)

# Optimize only the classifier
optimizer = optim.SGD(model.fc.parameters(), lr=1e-2, momentum=0.9)
How autograd encodes the history
Autograd is reverse automatic differentiation system. Conceptually, autograd records a graph recording all of the operations that created the data as you execute operations, giving you a directed acyclic graph whose leaves are the input tensors and roots are the output tensors. By tracing this graph from roots to leaves, you can automatically compute the gradients using the chain rule.

Internally, autograd represents this graph as a graph of Function objects (really expressions), which can be apply() ed to compute the result of evaluating the graph. When computing the forwards pass, autograd simultaneously performs the requested computations and builds up a graph representing the function that computes the gradient (the .grad_fn attribute of each torch.Tensor is an entry point into this graph). When the forwards pass is completed, we evaluate this graph in the backwards pass to compute the gradients.

An important thing to note is that the graph is recreated from scratch at every iteration, and this is exactly what allows for using arbitrary Python control flow statements, that can change the overall shape and size of the graph at every iteration. You don’t have to encode all possible paths before you launch the training - what you run is what you differentiate.

In-place operations with autograd
Supporting in-place operations in autograd is a hard matter, and we discourage their use in most cases. Autograd’s aggressive buffer freeing and reuse makes it very efficient and there are very few occasions when in-place operations actually lower memory usage by any significant amount. Unless you’re operating under heavy memory pressure, you might never need to use them.

There are two main reasons that limit the applicability of in-place operations:

In-place operations can potentially overwrite values required to compute gradients.

Every in-place operation actually requires the implementation to rewrite the computational graph. Out-of-place versions simply allocate new objects and keep references to the old graph, while in-place operations, require changing the creator of all inputs to the Function representing this operation. This can be tricky, especially if there are many Tensors that reference the same storage (e.g. created by indexing or transposing), and in-place functions will actually raise an error if the storage of modified inputs is referenced by any other Tensor.

In-place correctness checks
Every tensor keeps a version counter, that is incremented every time it is marked dirty in any operation. When a Function saves any tensors for backward, a version counter of their containing Tensor is saved as well. Once you access self.saved_tensors it is checked, and if it is greater than the saved value an error is raised. This ensures that if you’re using in-place functions and not seeing any errors, you can be sure that the computed gradients are correct.

Multithreaded Autograd
The autograd engine is responsible for running all the backward operations necessary to compute the backward pass. This section will describe all the details that can help you make the best use of it in a multithreaded environment.(this is relevant only for PyTorch 1.6+ as the behavior in previous version was different).

User could train their model with multithreading code (e.g. Hogwild training), and does not block on the concurrent backward computations, example code could be:

# Define a train function to be used in different threads
def train_fn():
    x = torch.ones(5, 5, requires_grad=True)
    # forward
    y = (x + 3) * (x + 4) * 0.5
    # backward
    y.sum().backward()
    # potential optimizer update


# User write their own threading code to drive the train_fn
threads = []
for _ in range(10):
    p = threading.Thread(target=train_fn, args=())
    p.start()
    threads.append(p)

for p in threads:
    p.join()
Note that some behaviors that user should be aware of:

Concurrency on CPU
When you run backward() or grad() via python or C++ API in multiple threads on CPU, you are expecting to see extra concurrency instead of serializing all the backward calls in a specific order during execution (behavior before PyTorch 1.6).

Non-determinism
If you are calling backward() on multiple thread concurrently but with shared inputs (i.e. Hogwild CPU training). Since parameters are automatically shared across threads, gradient accumulation might become non-deterministic on backward calls across threads, because two backward calls might access and try to accumulate the same .grad attribute. This is technically not safe, and it might result in racing condition and the result might be invalid to use.

But this is expected pattern if you are using the multithreading approach to drive the whole training process but using shared parameters, user who use multithreading should have the threading model in mind and should expect this to happen. User could use the functional API torch.autograd.grad() to calculate the gradients instead of backward() to avoid non-determinism.

Graph retaining
If part of the autograd graph is shared between threads, i.e. run first part of forward single thread, then run second part in multiple threads, then the first part of graph is shared. In this case different threads execute grad() or backward() on the same graph might have issue of destroying the graph on the fly of one thread, and the other thread will crash in this case. Autograd will error out to the user similar to what call backward() twice with out retain_graph=True, and let the user know they should use retain_graph=True.

Thread Safety on Autograd Node
Since Autograd allows the caller thread to drive its backward execution for potential parallelism, it’s important that we ensure thread safety on CPU with parallel backwards that share part/whole of the GraphTask.

Custom Python autograd.function is automatically thread safe because of GIL. for built-in C++ Autograd Nodes(e.g. AccumulateGrad, CopySlices) and custom autograd::Function, the Autograd Engine uses thread mutex locking to protect thread safety on autograd Nodes that might have state write/read.

No thread safety on C++ hooks
Autograd relies on the user to write thread safe C++ hooks. If you want the hook to be correctly applied in multithreading environment, you will need to write proper thread locking code to ensure the hooks are thread safe.

Autograd for Complex Numbers
The short version:

When you use PyTorch to differentiate any function f(z)f(z) with complex domain and/or codomain, the gradients are computed under the assumption that the function is a part of a larger real-valued loss function g(input)=Lg(input)=L . The gradient computed is \frac{\partial L}{\partial z^*} 
∂z 
∗
 
∂L
​	
  (note the conjugation of z), the negative of which is precisely the direction of steepest descent used in Gradient Descent algorithm. Thus, all the existing optimizers work out of the box with complex parameters.

This convention matches TensorFlow’s convention for complex differentiation, but is different from JAX (which computes \frac{\partial L}{\partial z} 
∂z
∂L
​	
  ).

If you have a real-to-real function which internally uses complex operations, the convention here doesn’t matter: you will always get the same result that you would have gotten if it had been implemented with only real operations.

If you are curious about the mathematical details, or want to know how to define complex derivatives in PyTorch, read on.

What are complex derivatives?
The mathematical definition of complex-differentiability takes the limit definition of a derivative and generalizes it to operate on complex numbers. Consider a function f: ℂ → ℂf:C→C ,

`f(z=x+yj) = u(x, y) + v(x, y)j`
‘f(z=x+yj)=u(x,y)+v(x,y)j‘
where uu and vv are two variable real valued functions.

Using the derivative definition, we can write:

f'(z) = \lim_{h \to 0, h \in C} \frac{f(z+h) - f(z)}{h}
f 
′
 (z)= 
h→0,h∈C
lim
​	
  
h
f(z+h)−f(z)
​	
 
In order for this limit to exist, not only must uu and vv must be real differentiable, but ff must also satisfy the Cauchy-Riemann equations. In other words: the limit computed for real and imaginary steps (hh ) must be equal. This is a more restrictive condition.

The complex differentiable functions are commonly known as holomorphic functions. They are well behaved, have all the nice properties that you’ve seen from real differentiable functions, but are practically of no use in the optimization world. For optimization problems, only real valued objective functions are used in the research community since complex numbers are not part of any ordered field and so having complex valued loss does not make much sense.

It also turns out that no interesting real-valued objective fulfill the Cauchy-Riemann equations. So the theory with homomorphic function cannot be used for optimization and most people therefore use the Wirtinger calculus.

Wirtinger Calculus comes in picture …
So, we have this great theory of complex differentiability and holomorphic functions, and we can’t use any of it at all, because many of the commonly used functions are not holomorphic. What’s a poor mathematician to do? Well, Wirtinger observed that even if f(z)f(z) isn’t holomorphic, one could rewrite it as a two variable function f(z, z*)f(z,z∗) which is always holomorphic. This is because real and imaginary of the components of zz can be expressed in terms of zz and z^*z 
∗
  as:

\begin{aligned} Re(z) &= \frac {z + z^*}{2} \\ Im(z) &= \frac {z - z^*}{2j} \end{aligned}
Re(z)
Im(z)
​	
  
= 
2
z+z 
∗
 
​	
 
= 
2j
z−z 
∗
 
​	
 
​	
 
Wirtinger calculus suggests to study f(z, z^*)f(z,z 
∗
 ) instead, which is guaranteed to be holomorphic if ff was real differentiable (another way to think of it is as a change of coordinate system, from f(x, y)f(x,y) to f(z, z^*)f(z,z 
∗
 ) .) This function has partial derivatives \frac{\partial }{\partial z} 
∂z
∂
​	
  and \frac{\partial}{\partial z^{*}} 
∂z 
∗
 
∂
​	
  . We can use the chain rule to establish a relationship between these partial derivatives and the partial derivatives w.r.t., the real and imaginary components of zz .

\begin{aligned} \frac{\partial }{\partial x} &= \frac{\partial z}{\partial x} * \frac{\partial }{\partial z} + \frac{\partial z^*}{\partial x} * \frac{\partial }{\partial z^*} \\ &= \frac{\partial }{\partial z} + \frac{\partial }{\partial z^*} \\ \\ \frac{\partial }{\partial y} &= \frac{\partial z}{\partial y} * \frac{\partial }{\partial z} + \frac{\partial z^*}{\partial y} * \frac{\partial }{\partial z^*} \\ &= 1j * (\frac{\partial }{\partial z} - \frac{\partial }{\partial z^*}) \end{aligned}
∂x
∂
​	
 
∂y
∂
​	
 
​	
  
= 
∂x
∂z
​	
 ∗ 
∂z
∂
​	
 + 
∂x
∂z 
∗
 
​	
 ∗ 
∂z 
∗
 
∂
​	
 
= 
∂z
∂
​	
 + 
∂z 
∗
 
∂
​	
 
= 
∂y
∂z
​	
 ∗ 
∂z
∂
​	
 + 
∂y
∂z 
∗
 
​	
 ∗ 
∂z 
∗
 
∂
​	
 
=1j∗( 
∂z
∂
​	
 − 
∂z 
∗
 
∂
​	
 )
​	
 
From the above equations, we get:

\begin{aligned} \frac{\partial }{\partial z} &= 1/2 * (\frac{\partial }{\partial x} - 1j * \frac{\partial }{\partial y}) \\ \frac{\partial }{\partial z^*} &= 1/2 * (\frac{\partial }{\partial x} + 1j * \frac{\partial }{\partial y}) \end{aligned}
∂z
∂
​	
 
∂z 
∗
 
∂
​	
 
​	
  
=1/2∗( 
∂x
∂
​	
 −1j∗ 
∂y
∂
​	
 )
=1/2∗( 
∂x
∂
​	
 +1j∗ 
∂y
∂
​	
 )
​	
 
which is the classic definition of Wirtinger calculus that you would find on Wikipedia.

There are a lot of beautiful consequences of this change.

For one, the Cauchy-Riemann equations translate into simply saying that \frac{\partial f}{\partial z^*} = 0 
∂z 
∗
 
∂f
​	
 =0 (that is to say, the function ff can be written entirely in terms of zz , without making reference to z^*z 
∗
  ).

Another important (and somewhat counterintuitive) result, as we’ll see later, is that when we do optimization on a real-valued loss, the step we should take while making variable update is given by \frac{\partial Loss}{\partial z^*} 
∂z 
∗
 
∂Loss
​	
  (not \frac{\partial Loss}{\partial z} 
∂z
∂Loss
​	
  ).

For more reading, check out: https://arxiv.org/pdf/0906.4835.pdf

How is Wirtinger Calculus useful in optimization?
Researchers in audio and other fields, more commonly, use gradient descent to optimize real valued loss functions with complex variables. Typically, these people treat the real and imaginary values as separate channels that can be updated. For a step size s/2s/2 and loss LL , we can write the following equations in ℝ^2R 
2
  :

\begin{aligned} x_{n+1} &= x_n - (s/2) * \frac{\partial L}{\partial x} \\ y_{n+1} &= y_n - (s/2) * \frac{\partial L}{\partial y} \end{aligned}
x 
n+1
​	
 
y 
n+1
​	
 
​	
  
=x 
n
​	
 −(s/2)∗ 
∂x
∂L
​	
 
=y 
n
​	
 −(s/2)∗ 
∂y
∂L
​	
 
​	
 
How do these equations translate into complex space ℂC ?

\begin{aligned} z_{n+1} &= x_n - (s/2) * \frac{\partial L}{\partial x} + 1j * (y_n - (s/2) * \frac{\partial L}{\partial y}) \\ &= z_n - s * 1/2 * (\frac{\partial L}{\partial x} + j \frac{\partial L}{\partial y}) \\ &= z_n - s * \frac{\partial L}{\partial z^*} \end{aligned}
z 
n+1
​	
 
​	
  
=x 
n
​	
 −(s/2)∗ 
∂x
∂L
​	
 +1j∗(y 
n
​	
 −(s/2)∗ 
∂y
∂L
​	
 )
=z 
n
​	
 −s∗1/2∗( 
∂x
∂L
​	
 +j 
∂y
∂L
​	
 )
=z 
n
​	
 −s∗ 
∂z 
∗
 
∂L
​	
 
​	
 
Something very interesting has happened: Wirtinger calculus tells us that we can simplify the complex variable update formula above to only refer to the conjugate Wirtinger derivative \frac{\partial L}{\partial z^*} 
∂z 
∗
 
∂L
​	
  , giving us exactly the step we take in optimization.

Because the conjugate Wirtinger derivative gives us exactly the correct step for a real valued loss function, PyTorch gives you this derivative when you differentiate a function with a real valued loss.

How does PyTorch compute the conjugate Wirtinger derivative?
Typically, our derivative formulas take in grad_output as an input, representing the incoming Vector-Jacobian product that we’ve already computed, aka, \frac{\partial L}{\partial s^*} 
∂s 
∗
 
∂L
​	
  , where LL is the loss of the entire computation (producing a real loss) and ss is the output of our function. The goal here is to compute \frac{\partial L}{\partial z^*} 
∂z 
∗
 
∂L
​	
  , where zz is the input of the function. It turns out that in the case of real loss, we can get away with only calculating \frac{\partial L}{\partial z^*} 
∂z 
∗
 
∂L
​	
  , even though the chain rule implies that we also need to have access to \frac{\partial L}{\partial z^*} 
∂z 
∗
 
∂L
​	
  . If you want to skip this derivation, look at the last equation in this section and then skip to the next section.

Let’s continue working with f: ℂ → ℂf:C→C defined as f(z) = f(x+yj) = u(x, y) + v(x, y)jf(z)=f(x+yj)=u(x,y)+v(x,y)j . As discussed above, autograd’s gradient convention is centered around optimization for real valued loss functions, so let’s assume ff is a part of larger real valued loss function gg . Using chain rule, we can write:

(1)
\frac{\partial L}{\partial z^*} = \frac{\partial L}{\partial u} * \frac{\partial u}{\partial z^*} + \frac{\partial L}{\partial v} * \frac{\partial v}{\partial z^*}
∂z 
∗
 
∂L
​	
 = 
∂u
∂L
​	
 ∗ 
∂z 
∗
 
∂u
​	
 + 
∂v
∂L
​	
 ∗ 
∂z 
∗
 
∂v
​	
 
Now using Wirtinger derivative definition, we can write:

\begin{aligned} \frac{\partial L}{\partial s} = 1/2 * (\frac{\partial L}{\partial u} - \frac{\partial L}{\partial v} j) \\ \frac{\partial L}{\partial s^*} = 1/2 * (\frac{\partial L}{\partial u} + \frac{\partial L}{\partial v} j) \end{aligned}
∂s
∂L
​	
 =1/2∗( 
∂u
∂L
​	
 − 
∂v
∂L
​	
 j)
∂s 
∗
 
∂L
​	
 =1/2∗( 
∂u
∂L
​	
 + 
∂v
∂L
​	
 j)
​	
 
It should be noted here that since uu and vv are real functions, and LL is real by our assumption that ff is a part of a real valued function, we have:

(2)
(\frac{\partial L}{\partial s})^* = \frac{\partial L}{\partial s^*}
( 
∂s
∂L
​	
 ) 
∗
 = 
∂s 
∗
 
∂L
​	
 
i.e., \frac{\partial L}{\partial s} 
∂s
∂L
​	
  equals to grad\_output^*grad_output 
∗
  .

Solving the above equations for \frac{\partial L}{\partial u} 
∂u
∂L
​	
  and \frac{\partial L}{\partial v} 
∂v
∂L
​	
  , we get:

(3)
\begin{aligned} \frac{\partial L}{\partial u} = \frac{\partial L}{\partial s} + \frac{\partial L}{\partial s^*} \\ \frac{\partial L}{\partial v} = -1j * (\frac{\partial L}{\partial s} - \frac{\partial L}{\partial s^*}) \end{aligned}
∂u
∂L
​	
 = 
∂s
∂L
​	
 + 
∂s 
∗
 
∂L
​	
 
∂v
∂L
​	
 =−1j∗( 
∂s
∂L
​	
 − 
∂s 
∗
 
∂L
​	
 )
​	
 
Substituting (3) in (1), we get:

\begin{aligned} \frac{\partial L}{\partial z^*} &= (\frac{\partial L}{\partial s} + \frac{\partial L}{\partial s^*}) * \frac{\partial u}{\partial z^*} - 1j * (\frac{\partial L}{\partial s} - \frac{\partial L}{\partial s^*}) * \frac{\partial v}{\partial z^*} \\ &= \frac{\partial L}{\partial s} * (\frac{\partial u}{\partial z^*} + \frac{\partial v}{\partial z^*} j) + \frac{\partial L}{\partial s^*} * (\frac{\partial u}{\partial z^*} - \frac{\partial v}{\partial z^*} j) \\ &= \frac{\partial L}{\partial s^*} * \frac{\partial (u + vj)}{\partial z^*} + \frac{\partial L}{\partial s} * \frac{\partial (u + vj)^*}{\partial z^*} \\ &= \frac{\partial L}{\partial s} * \frac{\partial s}{\partial z^*} + \frac{\partial L}{\partial s^*} * \frac{\partial s^*}{\partial z^*} \\ \end{aligned}
∂z 
∗
 
∂L
​	
 
​	
  
=( 
∂s
∂L
​	
 + 
∂s 
∗
 
∂L
​	
 )∗ 
∂z 
∗
 
∂u
​	
 −1j∗( 
∂s
∂L
​	
 − 
∂s 
∗
 
∂L
​	
 )∗ 
∂z 
∗
 
∂v
​	
 
= 
∂s
∂L
​	
 ∗( 
∂z 
∗
 
∂u
​	
 + 
∂z 
∗
 
∂v
​	
 j)+ 
∂s 
∗
 
∂L
​	
 ∗( 
∂z 
∗
 
∂u
​	
 − 
∂z 
∗
 
∂v
​	
 j)
= 
∂s 
∗
 
∂L
​	
 ∗ 
∂z 
∗
 
∂(u+vj)
​	
 + 
∂s
∂L
​	
 ∗ 
∂z 
∗
 
∂(u+vj) 
∗
 
​	
 
= 
∂s
∂L
​	
 ∗ 
∂z 
∗
 
∂s
​	
 + 
∂s 
∗
 
∂L
​	
 ∗ 
∂z 
∗
 
∂s 
∗
 
​	
 
​	
 
Using (2), we get:

(4)
\begin{aligned} \frac{\partial L}{\partial z^*} &= (\frac{\partial L}{\partial s^*})^* * \frac{\partial s}{\partial z^*} + \frac{\partial L}{\partial s^*} * (\frac{\partial s}{\partial z})^* \\ &= \boxed{ (grad\_output)^* * \frac{\partial s}{\partial z^*} + grad\_output * {(\frac{\partial s}{\partial z})}^* } \\ \end{aligned}
∂z 
∗
 
∂L
​	
 
​	
  
=( 
∂s 
∗
 
∂L
​	
 ) 
∗
 ∗ 
∂z 
∗
 
∂s
​	
 + 
∂s 
∗
 
∂L
​	
 ∗( 
∂z
∂s
​	
 ) 
∗
 
= 
(grad_output) 
∗
 ∗ 
∂z 
∗
 
∂s
​	
 +grad_output∗( 
∂z
∂s
​	
 ) 
∗
 
​	
 
​	
 
This last equation is the important one for writing your own gradients, as it decomposes our derivative formula into a simpler one that is easy to compute by hand.

How can I write my own derivative formula for a complex function?
The above boxed equation gives us the general formula for all derivatives on complex functions. However, we still need to compute \frac{\partial s}{\partial z} 
∂z
∂s
​	
  and \frac{\partial s}{\partial z^*} 
∂z 
∗
 
∂s
​	
  . There are two ways you could do this:

The first way is to just use the definition of Wirtinger derivatives directly and calculate \frac{\partial s}{\partial z} 
∂z
∂s
​	
  and \frac{\partial s}{\partial z^*} 
∂z 
∗
 
∂s
​	
  by using \frac{\partial s}{\partial x} 
∂x
∂s
​	
  and \frac{\partial s}{\partial y} 
∂y
∂s
​	
  (which you can compute in the normal way).

The second way is to use the change of variables trick and rewrite f(z)f(z) as a two variable function f(z, z^*)f(z,z 
∗
 ) , and compute the conjugate Wirtinger derivatives by treating zz and z^*z 
∗
  as independent variables. This is often easier; for example, if the function in question is holomorphic, only zz will be used (and \frac{\partial s}{\partial z^*} 
∂z 
∗
 
∂s
​	
  will be zero).

Let’s consider the function f(z = x + yj) = c * z = c * (x+yj)f(z=x+yj)=c∗z=c∗(x+yj) as an example, where c \in ℝc∈R .

Using the first way to compute the Wirtinger derivatives, we have.

\begin{aligned} \frac{\partial s}{\partial z} &= 1/2 * (\frac{\partial s}{\partial x} - \frac{\partial s}{\partial y} j) \\ &= 1/2 * (c - (c * 1j) * 1j) \\ &= c \\ \\ \\ \frac{\partial s}{\partial z^*} &= 1/2 * (\frac{\partial s}{\partial x} + \frac{\partial s}{\partial y} j) \\ &= 1/2 * (c + (c * 1j) * 1j) \\ &= 0 \\ \end{aligned}
∂z
∂s
​	
 
∂z 
∗
 
∂s
​	
 
​	
  
=1/2∗( 
∂x
∂s
​	
 − 
∂y
∂s
​	
 j)
=1/2∗(c−(c∗1j)∗1j)
=c
=1/2∗( 
∂x
∂s
​	
 + 
∂y
∂s
​	
 j)
=1/2∗(c+(c∗1j)∗1j)
=0
​	
 
Using (4), and grad_output = 1.0 (which is the default grad output value used when backward() is called on a scalar output in PyTorch), we get:

\frac{\partial L}{\partial z^*} = 1 * 0 + 1 * c = c
∂z 
∗
 
∂L
​	
 =1∗0+1∗c=c
Using the second way to compute Wirtinger derivatives, we directly get:

\begin{aligned} \frac{\partial s}{\partial z} &= \frac{\partial (c*z)}{\partial z} \\ &= c \\ \frac{\partial s}{\partial z^*} &= \frac{\partial (c*z)}{\partial z^*} \\ &= 0 \end{aligned}
∂z
∂s
​	
 
∂z 
∗
 
∂s
​	
 
​	
  
= 
∂z
∂(c∗z)
​	
 
=c
= 
∂z 
∗
 
∂(c∗z)
​	
 
=0
​	
 
And using (4) again, we get \frac{\partial L}{\partial z^*} = c 
∂z 
∗
 
∂L
​	
 =c . As you can see, the second way involves lesser calculations, and comes in more handy for faster calculations.

What about cross-domain functions?
Some functions map from complex inputs to real outputs, or vice versa. These functions form a special case of (4), which we can derive using the chain rule:

For f: ℂ → ℝf:C→R , we get:

\frac{\partial L}{\partial z^*} = 2 * grad\_output * \frac{\partial s}{\partial z^{*}}
∂z 
∗
 
∂L
​	
 =2∗grad_output∗ 
∂z 
∗
 
∂s
​	
 
For f: ℝ → ℂf:R→C , we get:

\frac{\partial L}{\partial z^*} = 2 * Re(grad\_out^* * \frac{\partial s}{\partial z^{*}})
∂z 
∗
 
∂L
​	
 =2∗Re(grad_out
