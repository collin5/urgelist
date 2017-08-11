import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { CommonModule } from '@angular/common';

@NgModule({
    declarations: [],
    imports:[
        FormsModule,
        CommonModule,
        HttpModule
    ],
    exports:[
        FormsModule,
        CommonModule,
        HttpModule
    ]
})
export class SharedModule{}
