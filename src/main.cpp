#include "GarrysMod/Lua/Interface.h"
#include "Console.hpp"
#include <Python.h>

using namespace GarrysMod::Lua;
using std::to_string;

/*

require( "example" );

MsgN( TestFunction() );

MsgN( TestFunction( 24.75 ) );

*/
/*
int MyExampleFunction( lua_State* state )
{
	if ( LUA->IsType( 1, Type::NUMBER ) )
	{
		char strOut[512];
		float fNumber = LUA->GetNumber( 1 );
		sprintf( strOut, "Thanks for the number - I love %f!!", fNumber );
		LUA->PushString( strOut );
		return 1;
	}

	LUA->PushString( "This string is returned" );
	return 1;
}*/


GMOD_MODULE_OPEN() {
	/*
	LUA->PushSpecial( GarrysMod::Lua::SPECIAL_GLOB );	// Push global table
	LUA->PushString( "TestFunction" );					// Push Name
	LUA->PushCFunction( MyExampleFunction );			// Push function
	LUA->SetTable( -3 );								// Set the table */

	Console cons(LUA);

	cons.log("Binary module loaded");

	Py_Initialize();
	cons.log("Python initialized!");

	// PyRun_SimpleString("import os;print('hi there');os.system('pause')");
	PyRun_SimpleString(("import sys; sys.lua_interface_addr = " + to_string((int) LUA)).c_str());
	cons.log("Set sys.lua_interface_addr to " + to_string((int) LUA));

	return 0;
}

GMOD_MODULE_CLOSE() {
	Console cons(LUA);

	cons.log("Binary module shutting down.");

	Py_FinalizeEx();
	cons.log("Python finalized!");

	return 0;
}
