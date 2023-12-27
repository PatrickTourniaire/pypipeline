.. _getting_started:

Getting Started
===============

Quick Start Guide
-----------------

The following is a basic tutorial to showcase how one can build a very simple forward propagating pipeline. Which defines
a three stage pipeline with a controller to iterate oer it.

Tutorial
--------

First it is good practise to define the schemas which will communicate between our three stages. But first let's import
the relevant packages.

Pipeline Schemas
^^^^^^^^^^^^^^^^

.. code-block:: python
  :caption: Import Relevant Packages

  from dataclasses import dataclass
  from typing import Tuple

  from pypipeline.schemas import BaseSchema
  from pypipeline.schemas.fields import field_perishable, field_persistance
  from pypipeline.stages import IInitStage, ITerminalStage, IForwardStage
  from pypipeline.controlers import BaseController

Then we can define the data schemas the following way.

.. code-block:: python
  :caption: Define Data Schemas

  @dataclass
  class TestInput(BaseSchema):
      testA: str = field_persistance()
      testB: str = field_perishable()
      testC: str = field_persistance()


  @dataclass
  class TestOutput(BaseSchema):
      testA: str = field_persistance()
      testC: str = field_perishable()
      testY: str = field_perishable()


  @dataclass
  class TestTerminalOutput(BaseSchema):
      testA: str = field_persistance()
      testD: str = field_persistance()

Pipeline Stages
^^^^^^^^^^^^^^^

Now that we have defined the pipeline schemas we can use these as types to create linkes
for the data transfer between stages. Which will make it easier for us to deal with types
and data in the pipeline as everything can simply be changed in the schemas.

.. code-block:: python
  :caption: Pipeline Stages

  class TerminalStage(ITerminalStage[TestOutput, TestTerminalOutput]):
    def compute(self) -> None:
        self.test = ""

    def get_output(self) -> TestTerminalOutput:
        _carry = self.input.get_carry()
        return TestTerminalOutput(**_carry, testD="testD")

  class ForwardStage(IForwardStage[TestOutput, TestOutput, TerminalStage]):
      def compute(self) -> None:
          return super().compute()

      def get_output(self) -> Tuple[TerminalStage, TestOutput]:
          _carry = self.input.get_carry()
          return TerminalStage(), TestOutput(**_carry)


  class InitStage(IInitStage[TestInput, TestOutput, ForwardStage]):
      def compute(self) -> None:
          self.test = ""

      def get_output(self) -> Tuple[TerminalStage, TestOutput]:
          _carry = self.input.get_carry()
          return ForwardStage(), TestOutput(**_carry, testY="testY")

Controler
^^^^^^^^^^

Then using just the instantiation of the init stage and its data schema, one can pass this to the
controler to start the pipeline and get the output of the final stage.

.. code-block:: python
  :caption: Controler

  test_input = TestInput(testA="testA", testB="testB", testC="testC")
  controller = BaseController(test_input, InitStage)

  controller.discover() # Prints the connection between the stages
  terminal_output, run_id = controller.start()

That's all! Now you can create a very basic forward propagating pipeline, and you can see how one can
maintain stages completely independently of eachother as long as the data schemas are updated/respected.
