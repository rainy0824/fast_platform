<template>
    <div id="app11">
      <div class="container">
        <div class="row">
          <div class="col-4">Column 1</div>
          <div class="col-4">Column 2</div>
          <div class="col-4">Column 3</div>
        </div>
      </div>
    </div>
  </template>
  
  <style>
    .container {
      width: 960px;
      margin: 0 auto;
    }
  
    .row {
      display: flex;
    }
  
    .col-4 {
      flex: 0 0 33.3333%;
    }
  </style>
  