// src/app/app-routing.module.ts

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { AddConnectionComponent } from './add-connection/add-connection.component';
import { ConfigureComponent } from './configure/configure.component';
import { SelectConnectionComponent } from './select-connection/select-connection.component';
import { TagManagerComponent } from './tag-manager/tag-manager.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'add-connection', component: AddConnectionComponent },
  { path: 'configure', component: ConfigureComponent },
  { path: 'select-connection', component: SelectConnectionComponent },
  { path: 'tag-manager', component: TagManagerComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
